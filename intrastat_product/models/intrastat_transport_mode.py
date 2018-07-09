# -*- coding: utf-8 -*-
# © 2011-2017 Akretion (http://www.akretion.com)
# © 2009-2017 Noviat (http://www.noviat.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# @author Luc de Meyer <info@noviat.com>

from odoo import models, fields, api


class IntrastatTransportMode(models.Model):
    _name = 'intrastat.transport_mode'
    _description = "Intrastat Transport Mode"
    _order = 'code'

    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Name', required=True, translate=True)
    description = fields.Char(string='Description', translate=True)

    @api.depends('name', 'code')
    def name_get(self):
        res = []
        for this in self:
            name = '%s. %s' % (this.code, this.name)
            res.append((this.id, name))
        return res

    _sql_constraints = [(
        'intrastat_transport_code_unique',
        'UNIQUE(code)',
        'Code must be unique.')]
