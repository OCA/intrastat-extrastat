# Copyright 2009-2020 Noviat nv/sa (www.noviat.com).
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# @author Luc de Meyer <info@noviat.com>

from odoo import fields, models


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    region_id = fields.Many2one(
        comodel_name="intrastat.region", string="Intrastat Region"
    )


class StockLocation(models.Model):
    _inherit = "stock.location"

    def get_intrastat_region(self):
        self.ensure_one()
        warehouse = self.env["stock.warehouse"].search(
            [("lot_stock_id", "parent_of", self.ids), ("region_id", "!=", False)],
            limit=1,
        )
        if warehouse:
            return warehouse.region_id
        return self.env["intrastat.region"]
