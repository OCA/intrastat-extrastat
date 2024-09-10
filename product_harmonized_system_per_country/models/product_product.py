#  Copyright (c) 2024 Groupe Voltaire
#  @author Emilie SOUTIRAS  <emilie.soutiras@groupevoltaire.com>
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    hs_code_ids = fields.Many2many(
        comodel_name="hs.code",
        relation="hs_code_pdt_tmpl_rel",
        column1="hs_code_id",
        column2="pdt_tmpl_id",
        string="H.S. Codes",
        help="Harmonised System Codes. This list is used to filter by "
        "destination country. If no code is set, the simple H.S. Code "
        "is used, otherwise those of the related product category.",
    )


class ProductProduct(models.Model):
    _inherit = "product.product"

    def get_hs_code_recursively(self):
        res = self.env["hs.code"]
        if self:
            self.ensure_one()
            if self.hs_code_ids:
                res = self.hs_code_ids.filter_per_country()
            else:
                res = super().get_hs_code_recursively()
        return res
