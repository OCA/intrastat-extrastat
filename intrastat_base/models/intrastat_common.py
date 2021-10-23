# Copyright 2010-2020 Akretion (<alexis.delattre@akretion.com>)
# Copyright 2009-2020 Noviat (http://www.noviat.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from io import BytesIO
from sys import exc_info
from traceback import format_exception

from lxml import etree

from odoo import _, api, fields, models, tools
from odoo.exceptions import UserError, ValidationError

logger = logging.getLogger(__name__)


class IntrastatCommon(models.AbstractModel):
    _name = "intrastat.common"
    _description = "Common functions for intrastat reports for products "
    "and services"

    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        required=True,
        states={"done": [("readonly", True)]},
        default=lambda self: self._default_company_id(),
    )
    company_country_code = fields.Char(
        compute="_compute_company_country_code",
        string="Company Country Code",
        readonly=True,
        store=True,
        help="Used in views and methods of localization modules.",
    )
    state = fields.Selection(
        selection=[("draft", "Draft"), ("done", "Done")],
        string="State",
        readonly=True,
        tracking=True,
        copy=False,
        default="draft",
        help="State of the declaration. When the state is set to 'Done', "
        "the parameters become read-only.",
    )
    note = fields.Text(
        string="Notes", help="You can add some comments here if you want."
    )

    year = fields.Char(
        string="Year", required=True, states={"done": [("readonly", True)]}
    )
    month = fields.Selection(
        selection=[
            ("01", "01"),
            ("02", "02"),
            ("03", "03"),
            ("04", "04"),
            ("05", "05"),
            ("06", "06"),
            ("07", "07"),
            ("08", "08"),
            ("09", "09"),
            ("10", "10"),
            ("11", "11"),
            ("12", "12"),
        ],
        string="Month",
        required=True,
        states={"done": [("readonly", True)]},
    )
    year_month = fields.Char(
        compute="_compute_year_month",
        string="Period",
        readonly=True,
        tracking=True,
        store=True,
        help="Year and month of the declaration.",
    )

    @api.model
    def _default_company_id(self):
        return self.env.company

    @api.depends("company_id")
    def _compute_company_country_code(self):
        for this in self:
            if this.company_id:
                if not this.company_id.country_id:
                    raise ValidationError(_("You must set company's country !"))
                this.company_country_code = this.company_id.country_id.code.lower()

    @api.depends("year", "month")
    def _compute_year_month(self):
        for this in self:
            if this.year and this.month:
                this.year_month = "-".join([this.year, this.month])

    @api.model
    @api.constrains("year")
    def _check_year(self):
        for this in self:
            if len(this.year) != 4 or this.year[0] != "2":
                raise ValidationError(_("Invalid Year !"))

    # The method _compute_numbers has been removed
    # because it was using a loop on lines, which is slow -> we should
    # use read_group() instead, but then the code depends on
    # the line object, so it can't be factorized here

    def _check_generate_xml(self):
        for this in self:
            if not this.company_id.partner_id.vat:
                raise UserError(
                    _("The VAT number is not set for the partner '%s'.")
                    % this.company_id.partner_id.name
                )

    @api.model
    def _check_xml_schema(self, xml_bytes, xsd_file):
        """Validate the XML file against the XSD"""
        xsd_etree_obj = etree.parse(tools.file_open(xsd_file, mode="rb"))
        official_schema = etree.XMLSchema(xsd_etree_obj)
        try:
            t = etree.parse(BytesIO(xml_bytes))
            official_schema.assertValid(t)
        except (etree.XMLSchemaParseError, etree.DocumentInvalid) as e:
            logger.warning("The XML file is invalid against the XML Schema Definition")
            logger.warning(xml_bytes)
            logger.warning(e)
            usererror = "{}\n\n{}".format(e.__class__.__name__, str(e))
            raise UserError(usererror)
        except Exception:
            error = _("Unknown Error")
            tb = "".join(format_exception(*exc_info()))
            error += "\n%s" % tb
            logger.warning(error)
            raise UserError(error)

    def _attach_xml_file(self, xml_bytes, declaration_name):
        """Attach the XML file to the report_intrastat_product/service
        object"""
        self.ensure_one()
        filename = "{}_{}.xml".format(self.year_month, declaration_name)
        attach = self.env["ir.attachment"].create(
            {
                "name": filename,
                "res_id": self.id,
                "res_model": self._name,
                "raw": xml_bytes,
            }
        )
        return attach.id

    def _unlink_attachments(self):
        atts = self.env["ir.attachment"].search(
            [("res_model", "=", self._name), ("res_id", "=", self.id)]
        )
        atts.unlink()

    # Method _open_attach_view() removed
    # Let's handle attachments like in l10n_fr_intrastat_service v14
    # with the field attachment_id on the declaration and the download
    # link directly on the form view of the declaration.

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
