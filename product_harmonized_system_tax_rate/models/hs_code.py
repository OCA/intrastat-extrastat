# Copyright 2021 Akretion France (http://www.akretion.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HSCode(models.Model):
    _inherit = "hs.code"

    tax_rate_ids = fields.One2many(
        comodel_name="hs.code.tax.rate",
        inverse_name="hs_code_id",
        string="Tax Rates",
    )
