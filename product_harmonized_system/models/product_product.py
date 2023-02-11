# Copyright 2011-2022 Akretion (http://www.akretion.com)
# Copyright 2009-2022 Noviat (http://www.noviat.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# @author Luc de Meyer <info@noviat.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def get_hs_code_recursively(self):
        res = self.env["hs.code"]
        if self:
            self.ensure_one()
            if self.hs_code_id:
                res = self.hs_code_id
            elif self.categ_id:
                res = self.categ_id.get_hs_code_recursively()
        return res
