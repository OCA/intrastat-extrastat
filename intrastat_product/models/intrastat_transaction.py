# Copyright 2011-2017 Akretion (http://www.akretion.com)
# Copyright 2009-2018 Noviat (http://www.noviat.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# @author Luc de Meyer <info@noviat.com>

from odoo import api, fields, models


class IntrastatTransaction(models.Model):
    _name = 'intrastat.transaction'
    _description = "Intrastat Transaction"
    _order = 'code'
    _rec_name = 'display_name'
    _sql_constraints = [(
        'intrastat_transaction_code_unique',
        'UNIQUE(code, company_id)',
        'Code must be unique.')]

    code = fields.Char(string='Code', required=True)
    description = fields.Text(string='Description')
    display_name = fields.Char(
        compute='_compute_display_name_field', string="Display Name",
        readonly=True, store=True)
    company_id = fields.Many2one(
        comodel_name='res.company', string='Company',
        default=lambda self: self.env['res.company']._company_default_get(
            'intrastat.transaction'))

    @api.multi
    @api.depends('code', 'description')
    def _compute_display_name_field(self):
        for this in self:
            display_name = this.code
            if this.description:
                display_name += ' ' + this.description
            this.display_name = len(display_name) > 55 \
                and display_name[:55] + '...' \
                or display_name
