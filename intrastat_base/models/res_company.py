# Copyright 2013-2022 Akretion France (http://www.akretion.com/)
# @author: <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from io import BytesIO
from sys import exc_info
from traceback import format_exception

from lxml import etree

from odoo import _, api, fields, models, tools
from odoo.exceptions import UserError, ValidationError

logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    _inherit = "res.company"

    intrastat_remind_user_ids = fields.Many2many(
        comodel_name="res.users",
        relation="company_intrastat_reminder_user_rel",
        column1="company_id",
        column2="user_id",
        string="Users Receiving the Intrastat Reminder",
        help="List of Odoo users who will receive a notification to "
        "remind them about the Intrastat declaration.",
    )
    intrastat_email_list = fields.Char(
        compute="_compute_intrastat_email_list",
        string="List of emails of Users Receiving the Intrastat Reminder",
    )

    @api.depends("intrastat_remind_user_ids", "intrastat_remind_user_ids.email")
    def _compute_intrastat_email_list(self):
        for this in self:
            emails = []
            for user in this.intrastat_remind_user_ids:
                if user.email:
                    emails.append(user.email)
            this.intrastat_email_list = ",".join(emails)

    @api.constrains("intrastat_remind_user_ids")
    def _check_intrastat_remind_users(self):
        for this in self:
            for user in this.intrastat_remind_user_ids:
                if not user.email:
                    raise ValidationError(
                        _("Missing e-mail address on user '%s'.") % (user.name)
                    )

    @api.model
    def _intrastat_check_xml_schema(self, xml_bytes, xsd_file):
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
            raise UserError(usererror) from e
        except Exception as e:
            error = _("Unknown Error")
            tb = "".join(format_exception(*exc_info()))
            error += "\n%s" % tb
            logger.warning(error)
            raise UserError(error) from e
