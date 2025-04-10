# Copyright 2021 Akretion France (http://www.akretion.com)
# @author Olivier Nibart <olivier.nibart@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HSCodeTaxRate(models.Model):
    _name = "hs.code.tax.rate"
    _description = "H.S. Code Tax Rate"
    _order = "hs_code_id, tax_rate"
    _sql_constraints = [
        (
            "hs_code_origin_country_uniq",
            "unique(origin_country_id, hs_code_id)",
            "H.S. Code/Country of Origin must be unique",
        )
    ]

    hs_code_id = fields.Many2one(
        "hs.code",
        string="H.S. Code",
        required=True,
        ondelete="restrict",
        help="Harmonised System Code. Nomenclature is "
        "available from the World Customs Organisation, see "
        "http://www.wcoomd.org/.",
    )

    origin_country_id = fields.Many2one(
        "res.country",
        string="Country of Origin",
        required=True,
        help="Country of origin of the product i.e. product " "'made in ____'.",
    )

    tax_rate = fields.Float(
        string="Tax Rate %",
        required=True,
        help="Tax rate percentage for this H.S. Code / Country of Origin.",
    )
