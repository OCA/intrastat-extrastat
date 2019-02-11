# Copyright 2011-2017 Akretion (http://www.akretion.com)
# Copyright 2009-2019 Noviat (http://www.noviat.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# @author Luc de Meyer <info@noviat.com>

from odoo import api, fields, models


class IntrastatTransportMode(models.Model):
    _name = 'intrastat.transport_mode'
    _description = "Intrastat Transport Mode"
    _rec_name = 'display_name'
    _order = 'code'
    _sql_constraints = [(
        'intrastat_transport_code_unique',
        'UNIQUE(code)',
        'Code must be unique.')]

    display_name = fields.Char(
        string='Display Name', compute='_compute_display_name', store=True,
        readonly=True)
    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Name', required=True, translate=True)
    description = fields.Char(string='Description', translate=True)

    @api.multi
    @api.depends('name', 'code')
    def _compute_display_name(self):
        for this in self:
            this.display_name = '%s. %s' % (this.code, this.name)
