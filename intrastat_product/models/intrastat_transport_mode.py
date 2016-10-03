# -*- coding: utf-8 -*-
# © 2011-2017 Akretion (http://www.akretion.com)
# © 2009-2017 Noviat (http://www.noviat.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# @author Luc de Meyer <info@noviat.com>

from odoo import models, fields, api


class IntrastatTransportMode(models.Model):
    _name = 'intrastat.transport_mode'
    _description = "Intrastat Transport Mode"
    _rec_name = 'display_name'
    _order = 'code'

    display_name = fields.Char(
        string='Display Name', compute='_display_name', store=True,
        readonly=True)
    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Name', required=True, translate=True)
    description = fields.Char(string='Description', translate=True)

    @api.multi
    @api.depends('name', 'code')
    def _display_name(self):
        for this in self:
            this.display_name = '%s. %s' % (this.code, this.name)

    _sql_constraints = [(
        'intrastat_transport_code_unique',
        'UNIQUE(code)',
        'Code must be unique.')]
