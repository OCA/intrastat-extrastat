#  Copyright (c) 2024 Groupe Voltaire
#  @author Emilie SOUTIRAS  <emilie.soutiras@groupevoltaire.com>
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class HSCode(models.Model):
    _inherit = "hs.code"

    country_id = fields.Many2one(
        comodel_name="res.country", string="Applicable country"
    )
    pdt_categ_ids = fields.Many2many(
        comodel_name="product.category",
        relation="hs_code_pdt_category_rel",
        column1="pdt_categ_id",
        column2="hs_code_id",
        string="Product Categories on H.S. Codes list",
        readonly=True,
    )
    pdt_tmpl_ids = fields.Many2many(
        comodel_name="product.template",
        relation="hs_code_pdt_tmpl_rel",
        column1="pdt_tmpl_id",
        column2="hs_code_id",
        string="Products on H.S. Codes list",
        readonly=True,
    )

    @api.depends("product_categ_ids", "pdt_categ_ids")
    def _compute_product_categ_count(self):
        for code in self:
            code.product_categ_count = len(
                set(code.product_categ_ids.ids).union(set(code.pdt_categ_ids.ids))
            )

    @api.depends("product_tmpl_ids", "pdt_tmpl_ids")
    def _compute_product_tmpl_count(self):
        for code in self:
            code.product_tmpl_count = len(
                set(code.product_tmpl_ids.ids).union(set(code.pdt_tmpl_ids.ids))
            )

    def filter_per_country(self):
        country_id = self.env.context.get("hs_code_for_country", False)
        active_companies = self.env.context.get("allowed_company_ids")
        company_ids = [active_companies[0]] if active_companies else []
        company_ids += [False]
        if country_id:
            res = self.filtered(
                lambda hs: (not hs.country_id or hs.country_id.id == country_id)
                and (hs.company_id.id in company_ids)
            )
            res = (
                res.sorted()
                .sorted(key="company_id", reverse=True)
                .sorted(key="country_id", reverse=True)
            )
        else:
            res = self.filtered(lambda hs: (hs.company_id.id in company_ids))
            res = res.sorted(key="company_id", reverse=True)
        if res:
            res = res[0]
        return res
