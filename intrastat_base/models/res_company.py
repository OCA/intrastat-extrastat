# -*- coding: utf-8 -*-
# © 2013-2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ResCompany(models.Model):
    _inherit = "res.company"

    intrastat_remind_user_ids = fields.Many2many(
        'res.users', column1='company_id', column2='user_id',
        string="Users Receiving the Intrastat Reminder",
        help="List of Odoo users who will receive a notification to "
        "remind them about the Intrastat declaration.")
    intrastat_email_list = fields.Char(
        compute='_compute_intrastat_email_list',
        string='List of emails of Users Receiving the Intrastat Reminder')

    @api.multi
    @api.depends(
        'intrastat_remind_user_ids', 'intrastat_remind_user_ids.email')
    def _compute_intrastat_email_list(self):
        for this in self:
            emails = []
            for user in this.intrastat_remind_user_ids:
                if user.email:
                    emails.append(user.email)
            this.intrastat_email_list = ','.join(emails)

    @api.multi
    @api.constrains('intrastat_remind_user_ids')
    def _check_intrastat_remind_users(self):
        for this in self:
            for user in this.intrastat_remind_user_ids:
                if not user.email:
                    raise ValidationError(
                        _("Missing e-mail address on user '%s'.") %
                        (user.name))
