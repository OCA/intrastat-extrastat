# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models
from odoo.fields import first


class IntrastatProductDeclaration(models.Model):
    _inherit = "intrastat.product.declaration"

    def _get_product_origin_country(self, inv_line, notedict):
        """
        Retrieves the country of origin on the lot related to sale/purchase
        If not found, call back to original method
        """
        country = self.env["res.country"].browse()
        if inv_line.purchase_line_id and inv_line.purchase_line_id.move_ids:
            country = first(
                inv_line.purchase_line_id.move_ids.mapped("lot_ids")
            ).origin_country_id
        elif inv_line.sale_line_ids and inv_line.sale_line_ids.mapped("move_ids"):
            country = first(
                inv_line.sale_line_ids.mapped("move_ids.lot_ids")
            ).origin_country_id
        if country:
            return country
        return super()._get_product_origin_country(inv_line, notedict)
