# Copyright 2011-2020 Akretion France (http://www.akretion.com)
# Copyright 2009-2020 Noviat (http://www.noviat.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# @author Luc de Meyer <info@noviat.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    hs_code_id = fields.Many2one(
        "hs.code",
        string="H.S. Code",
        # company_dependent updated from True to False in 14.0.2.0.0
        # migration scripts provided
        company_dependent=False,
        ondelete="restrict",
        help="Harmonised System Code. If this code is not "
        "set on the product itself, it will be read here, on the "
        "related product category.",
    )

    def get_hs_code_recursively(self):
        self.ensure_one()
        if self.hs_code_id:
            res = self.hs_code_id
        elif self.parent_id:
            res = self.parent_id.get_hs_code_recursively()
        else:
            res = self.env["hs.code"]
        return res
