#  Copyright (c) 2024 Groupe Voltaire
#  @author Emilie SOUTIRAS  <emilie.soutiras@groupevoltaire.com>
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    hs_code = fields.Char(compute="_compute_hs_code", store=False)

    @api.depends(
        "hs_code_id", "hs_code_id.parent_id", "hs_code_id.child_ids", "categ_id"
    )
    def _compute_hs_code(self):
        for pdt_tmpl in self:
            if pdt_tmpl.hs_code_id:
                pdt_tmpl.hs_code = (
                    pdt_tmpl.hs_code_id.filter_per_country().hs_code or ""
                )
            else:
                pdt_tmpl.hs_code = (
                    pdt_tmpl.categ_id.get_hs_code_recursively().hs_code or ""
                )
