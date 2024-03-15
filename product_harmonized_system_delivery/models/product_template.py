# Copyright 2017-2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # IMPORTANT: Overwrites two Odoo standard fields
    hs_code = fields.Char(related="hs_code_id.hs_code", store=True)
    country_of_origin = fields.Many2one(related="origin_country_id", store=True)
