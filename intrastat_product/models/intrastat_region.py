# Copyright 2009-2018 Noviat nv/sa (www.noviat.com).
# @author Luc de Meyer <info@noviat.com>

from odoo import fields, models


class IntrastatRegion(models.Model):
    _name = 'intrastat.region'
    _description = "Intrastat Region"
    _sql_constraints = [
        ('intrastat_region_code_unique',
         'UNIQUE(code, country_id)',  # TODO add company_id ?
         'Code must be unique.')]

    code = fields.Char(string='Code', required=True)
    country_id = fields.Many2one(
        comodel_name='res.country',
        string='Country', required=True)
    name = fields.Char(string='Name', translate=True)
    description = fields.Char(string='Description')
    company_id = fields.Many2one(
        comodel_name='res.company', string='Company',
        default=lambda self: self.env['res.company']._company_default_get(
            'intrastat.region'))
