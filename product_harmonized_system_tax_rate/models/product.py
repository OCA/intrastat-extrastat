# Copyright 2021 Akretion France (http://www.akretion.com)
# @author Olivier Nibart <olivier.nibart@akretion.com>
# @author Raphaël Reverdy <raphael.reverdy@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    hs_code_tax_rate_id = fields.Many2one(
        "hs.code.tax.rate",
        compute="_compute_hs_code_tax_rate_id",
        string="H.S. Code Tax Rate Id",
        readonly=True,
        store=True,
    )

    hs_code_tax_rate = fields.Float(
        # helper for dependent modules
        related="hs_code_tax_rate_id.tax_rate",
    )

    hs_code_tax_rate_str = fields.Char(
        # used in the view
        string="H.S. Code Tax Rate",
        compute="_compute_hs_code_tax_rate_str",
    )

    @api.depends("origin_country_id", "hs_code_id", "hs_code_id.tax_rate_ids")
    def _compute_hs_code_tax_rate_id(self):
        for product in self:
            product.hs_code_tax_rate_id = product.hs_code_id.tax_rate_ids.filtered(
                lambda x, product=product: x.origin_country_id
                == product.origin_country_id
            )[:1]

    @api.depends("hs_code_tax_rate")
    def _compute_hs_code_tax_rate_str(self):
        for product in self:
            if product.hs_code_tax_rate_id:
                # test on hs_code_tax_rate_id to distinguish no value and 0%.
                product.hs_code_tax_rate_str = f"{product.hs_code_tax_rate} %"
            else:
                product.hs_code_tax_rate_str = ""
