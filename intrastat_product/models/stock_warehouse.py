# -*- coding: utf-8 -*-
# Copyright 2009-2017 Noviat
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    region_id = fields.Many2one(
        'intrastat.region',
        string='Intrastat region')
    country_code = fields.Char(
        related='company_id.country_id.code', readonly=True)


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
