# -*- coding: utf-8 -*-
# © 2011-2017 Akretion (http://www.akretion.com)
# © 2009-2017 Noviat (http://www.noviat.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# @author Luc de Meyer <info@noviat.com>

from odoo import models, fields


class IntrastatUnit(models.Model):
    _name = 'intrastat.unit'
    _description = 'Intrastat Supplementary Units'

    name = fields.Char(string='Name', required=True)
    description = fields.Char(string='Description', required=True)
    uom_id = fields.Many2one(
        'product.uom', string='Regular UoM',
        help="Select the regular Unit of Measure of Odoo that corresponds "
        "to this Intrastat Supplementary Unit.")
    active = fields.Boolean(string='Active', default=True)
