# -*- coding: utf-8 -*-
# © 2010-2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, tools, _
from odoo.exceptions import UserError
import logging

logger = logging.getLogger(__name__)


class IntrastatCommon(models.AbstractModel):
    _name = "intrastat.common"
    _description = "Common functions for intrastat reports for products "
    "and services"

    @api.multi
    @api.depends('declaration_line_ids.amount_company_currency')
    def _compute_numbers(self):
        for this in self:
            total_amount = 0  # it is an integer
            num_lines = 0
            for line in this.declaration_line_ids:
                total_amount += line.amount_company_currency
                num_lines += 1
            this.num_decl_lines = num_lines
            this.total_amount = total_amount

    @api.multi
    def _check_generate_lines(self):
        """Check wether all requirements are met for generating lines."""
        for this in self:
            if not this.company_id:
                raise UserError(_("Company not yet set on intrastat report."))
            company = this.company_id
            if not company.country_id:
                raise UserError(
                    _("The country is not set on the company '%s'.")
                    % company.name)
            if company.currency_id.name != 'EUR':
                raise UserError(
                    _("The company currency must be 'EUR', but is currently "
                      "'%s'.")
                    % company.currency_id.name)
        return True

    @api.multi
    def _check_generate_xml(self):
        for this in self:
            if not this.company_id.partner_id.vat:
                raise UserError(
                    _("The VAT number is not set for the partner '%s'.")
                    % this.company_id.partner_id.name)
        return True

    @api.model
    def _check_xml_schema(self, xml_string, xsd_file):
        '''Validate the XML file against the XSD'''
        from lxml import etree
        from StringIO import StringIO
        xsd_etree_obj = etree.parse(
            tools.file_open(xsd_file))
        official_schema = etree.XMLSchema(xsd_etree_obj)
        try:
            t = etree.parse(StringIO(xml_string))
            official_schema.assertValid(t)
        except Exception, e:
            # if the validation of the XSD fails, we arrive here
            logger = logging.getLogger(__name__)
            logger.warning(
                "The XML file is invalid against the XML Schema Definition")
            logger.warning(xml_string)
            logger.warning(e)
            raise UserError(
                _("The generated XML file is not valid against the official "
                    "XML Schema Definition. The generated XML file and the "
                    "full error have been written in the server logs. "
                    "Here is the error, which may give you an idea on the "
                    "cause of the problem : %s.")
                % str(e))
        return True

    @api.multi
    def _attach_xml_file(self, xml_string, declaration_name):
        '''Attach the XML file to the report_intrastat_product/service
        object'''
        self.ensure_one()
        import base64
        filename = '%s_%s.xml' % (self.year_month, declaration_name)
        attach = self.env['ir.attachment'].create({
            'name': filename,
            'res_id': self.id,
            'res_model': self._name,
            'datas': base64.encodestring(xml_string),
            'datas_fname': filename})
        return attach.id

    @api.multi
    def _unlink_attachments(self):
        atts = self.env['ir.attachment'].search(
            [('res_model', '=', self._name),
             ('res_id', '=', self.id)])
        atts.unlink()

    @api.model
    def _open_attach_view(self, attach_id, title='XML file'):
        '''Returns an action which opens the form view of the
        corresponding attachement'''
        action = {
            'name': title,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'ir.attachment',
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'current',
            'res_id': attach_id,
            }
        return action

    @api.multi
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

    @api.multi
    def send_reminder_email(self, mail_template_xmlid):
        mail_template = self.env.ref(mail_template_xmlid)
        for this in self:
            if this.company_id.intrastat_remind_user_ids:
                mail_template.send_mail(this.id)
                logger.info(
                    'Intrastat Reminder email has been sent (XMLID: %s).'
                    % mail_template_xmlid)
            else:
                logger.warning(
                    'The list of users receiving the Intrastat Reminder is '
                    'empty on company %s' % this.company_id.name)
        return True

    @api.multi
    def unlink(self):
        for intrastat in self:
            if intrastat.state == 'done':
                raise UserError(
                    _('Cannot delete the declaration %s '
                        'because it is in Done state') % self.year_month)
        return super(IntrastatCommon, self).unlink()


class IntrastatResultView(models.TransientModel):
    """
    Transient Model to display Intrastat Report results
    """
    _name = 'intrastat.result.view'

    note = fields.Text(
        string='Notes', readonly=True,
        default=lambda self: self._context.get('note'))
