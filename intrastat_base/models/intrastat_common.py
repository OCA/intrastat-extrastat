# Copyright 2010-2016 Akretion (<alexis.delattre@akretion.com>)
# Copyright 2009-2019 Noviat (http://www.noviat.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64
import logging
from io import BytesIO
from sys import exc_info
from traceback import format_exception

from lxml import etree

from odoo import _, api, fields, models, tools
from odoo.exceptions import UserError

logger = logging.getLogger(__name__)


class IntrastatCommon(models.AbstractModel):
    _name = "intrastat.common"
    _description = "Common functions for intrastat reports for products "
    "and services"

    @api.depends("declaration_line_ids.amount_company_currency")
    def _compute_numbers(self):
        for this in self:
            total_amount = 0  # it is an integer
            num_lines = 0
            for line in this.declaration_line_ids:
                total_amount += line.amount_company_currency
                num_lines += 1
            this.num_decl_lines = num_lines
            this.total_amount = total_amount

    def _check_generate_lines(self):
        """Check wether all requirements are met for generating lines."""
        for this in self:
            if not this.company_id:
                raise UserError(_("Company not yet set on intrastat report."))
            company = this.company_id
            if not company.country_id:
                raise UserError(
                    _("The country is not set on the company '%s'.") % company.name
                )
        return True

    def _check_generate_xml(self):
        for this in self:
            if not this.company_id.partner_id.vat:
                raise UserError(
                    _("The VAT number is not set for the partner '%s'.")
                    % this.company_id.partner_id.name
                )
        return True

    @api.model
    def _check_xml_schema(self, xml_string, xsd_file):
        """Validate the XML file against the XSD"""
        xsd_etree_obj = etree.parse(tools.file_open(xsd_file, mode="rb"))
        official_schema = etree.XMLSchema(xsd_etree_obj)
        try:
            t = etree.parse(BytesIO(xml_string))
            official_schema.assertValid(t)
        except (etree.XMLSchemaParseError, etree.DocumentInvalid) as e:
            logger.warning("The XML file is invalid against the XML Schema Definition")
            logger.warning(xml_string)
            logger.warning(e)
            usererror = "{}\n\n{}".format(e.__class__.__name__, str(e))
            raise UserError(usererror)
        except Exception:
            error = _("Unknown Error")
            tb = "".join(format_exception(*exc_info()))
            error += "\n%s" % tb
            logger.warning(error)
            raise UserError(error)

    def _attach_xml_file(self, xml_string, declaration_name):
        """Attach the XML file to the report_intrastat_product/service
        object"""
        self.ensure_one()
        filename = "{}_{}.xml".format(self.year_month, declaration_name)
        attach = self.env["ir.attachment"].create(
            {
                "name": filename,
                "res_id": self.id,
                "res_model": self._name,
                "datas": base64.encodestring(xml_string),
                "store_fname": filename,
            }
        )
        return attach.id

    def _unlink_attachments(self):
        atts = self.env["ir.attachment"].search(
            [("res_model", "=", self._name), ("res_id", "=", self.id)]
        )
        atts.unlink()

    @api.model
    def _open_attach_view(self, attach_id, title="XML file"):
        """Returns an action which opens the form view of the
        corresponding attachement"""
        action = {
            "name": title,
            "view_type": "form",
            "view_mode": "form",
            "res_model": "ir.attachment",
            "type": "ir.actions.act_window",
            "nodestroy": True,
            "target": "current",
            "res_id": attach_id,
        }
        return action

    def _generate_xml(self):
        """
        Inherit this method in the localization module
        to generate the INTRASTAT Declaration XML file

        Returns:
        string with XML data

        Call the _check_xml_schema() method
        before returning the XML string.
        """
        return False

    def send_reminder_email(self, mail_template_xmlid):
        mail_template = self.env.ref(mail_template_xmlid)
        for this in self:
            if this.company_id.intrastat_remind_user_ids:
                mail_template.send_mail(this.id)
                logger.info(
                    "Intrastat Reminder email has been sent (XMLID: %s)."
                    % mail_template_xmlid
                )
            else:
                logger.warning(
                    "The list of users receiving the Intrastat Reminder is "
                    "empty on company %s" % this.company_id.name
                )
        return True

    def unlink(self):
        for intrastat in self:
            if intrastat.state == "done":
                raise UserError(
                    _("Cannot delete the declaration %s " "because it is in Done state")
                    % self.year_month
                )
        return super().unlink()


class IntrastatResultView(models.TransientModel):
    """
    Transient Model to display Intrastat Report results
    """

    _name = "intrastat.result.view"
    _description = "Pop-up to show errors on intrastat report generation"

    note = fields.Text(
        string="Notes", readonly=True, default=lambda self: self._context.get("note")
    )
