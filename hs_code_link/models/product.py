# Copyright 2017 Camptocamp SA
# Copyright 2023 ForgeFlow <http://www.forgeflow.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # Make it compute non-stored as we will get the value from the bypassed company
    hs_code = fields.Char(compute="_compute_hs_code")

    @api.depends_context("force_company")
    def _compute_hs_code(self):
        for template in self:
            template.hs_code = template.hs_code_id.hs_code
