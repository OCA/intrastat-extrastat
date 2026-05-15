# Copyright 2009-2020 Noviat nv/sa (www.noviat.com).
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# @author Luc de Meyer <info@noviat.com>

from odoo import fields, models


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    region_id = fields.Many2one(
        comodel_name="intrastat.region", string="Intrastat Region"
    )
