# -*- coding: utf-8 -*-
# © 2009-2017 Noviat nv/sa (www.noviat.com).
# @author Luc de Meyer <info@noviat.com>

from odoo import models, fields


class IntrastatRegion(models.Model):
    _name = 'intrastat.region'
    _description = "Intrastat Region"

    code = fields.Char(string='Code', required=True)
    country_id = fields.Many2one(
        'res.country', string='Country', required=True)
    name = fields.Char(string='Name', translate=True)
    description = fields.Char(string='Description')
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env['res.company']._company_default_get(
            'intrastat.region'))

    _sql_constraints = [
        ('intrastat_region_code_unique',
         'UNIQUE(code, country_id)',  # TODO add company_id ?
         'Code must be unique.')]
