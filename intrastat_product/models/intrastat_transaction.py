# Copyright 2011-2017 Akretion France (http://www.akretion.com)
# Copyright 2009-2018 Noviat (http://www.noviat.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# @author Luc de Meyer <info@noviat.com>

from odoo import api, fields, models


class IntrastatTransaction(models.Model):
    _name = 'intrastat.transaction'
    _description = "Intrastat Transaction"
    _order = 'code'
    _sql_constraints = [(
        'intrastat_transaction_code_unique',
        'UNIQUE(code, company_id)',
        'Code must be unique.')]

    code = fields.Char(string='Code', required=True)
    description = fields.Text(string='Description')
    company_id = fields.Many2one(
        comodel_name='res.company', string='Company',
        default=lambda self: self.env['res.company']._company_default_get())

    @api.depends('code', 'description')
    def name_get(self):
        res = []
        for this in self:
            name = this.code
            if this.description:
                name += ' ' + this.description
            name = len(name) > 55 and name[:55] + '...' or name
            res.append((this.id, name))
        return res
