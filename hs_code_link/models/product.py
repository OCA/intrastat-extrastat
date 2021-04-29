# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # this field cannot be stored because hs_code_id is company dependent
    hs_code = fields.Char(related="hs_code_id.hs_code", readonly=True, store=False)
