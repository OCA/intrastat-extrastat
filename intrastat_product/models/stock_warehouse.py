# -*- coding: utf-8 -*-
# © 2009-2017 Noviat nv/sa (www.noviat.com).
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# @author Luc de Meyer <info@noviat.com>

from odoo import models, fields, api


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    region_id = fields.Many2one('intrastat.region', string='Intrastat Region')


class StockLocation(models.Model):
    _inherit = 'stock.location'

    @api.multi
    def get_intrastat_region(self):
        self.ensure_one()
        locations = self.search(
            [('parent_left', '<=', self.parent_left),
             ('parent_right', '>=', self.parent_right)])
        warehouses = self.env['stock.warehouse'].search([
            ('lot_stock_id', 'in', [x.id for x in locations]),
            ('region_id', '!=', False)])
        if warehouses:
            return warehouses[0].region_id
        return None
