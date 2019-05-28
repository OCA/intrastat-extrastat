# Copyright 2009-2018 Noviat nv/sa (www.noviat.com).
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# @author Luc de Meyer <info@noviat.com>

from odoo import fields, models


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    region_id = fields.Many2one(
        comodel_name='intrastat.region', string='Intrastat Region')


class StockLocation(models.Model):
    _inherit = 'stock.location'

    def get_intrastat_region(self):
        self.ensure_one()
        locations = self.search([('id', 'parent_of', self.id)])
        warehouses = self.env['stock.warehouse'].search([
            ('lot_stock_id', 'in', locations.ids),
            ('region_id', '!=', False)])
        if warehouses:
            return warehouses[0].region_id
        return None
