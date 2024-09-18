#  Copyright (c) 2024 Groupe Voltaire
#  @author Emilie SOUTIRAS  <emilie.soutiras@groupevoltaire.com>
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class HSCode(models.Model):
    _inherit = "hs.code"

    country_id = fields.Many2one(
        comodel_name="res.country", string="Applicable country"
    )
    parent_id = fields.Many2one(
        comodel_name="hs.code",
        string="Parent H.S. Code",
        ondelete="set null",
    )
    child_ids = fields.One2many(
        comodel_name="hs.code",
        inverse_name="parent_id",
        string="Child H.S. Codes related for other countries",
        copy=False,
    )
    related_hs_code_ids = fields.Many2many(
        comodel_name="hs.code",
        compute="_compute_related_hs_code",
        string="All related H.S. Codes",
    )

    def _compute_related_hs_code(self):
        for code in self:
            res = code | code.parent_id | code.child_ids
            if code.parent_id:
                res |= code.parent_id.child_ids
            code.related_hs_code_ids = res

    def filter_per_country(self):
        country_id = self.env.context.get("hs_code_for_country", False)
        active_companies = self.env.context.get("allowed_company_ids")
        company_ids = [active_companies[0]] if active_companies else []
        company_ids += [False]
        if country_id:
            self._compute_related_hs_code()
            res = self.related_hs_code_ids.filtered(
                lambda hs: (not hs.country_id or hs.country_id.id == country_id)
                and (hs.company_id.id in company_ids)
            )
            res = (
                res.sorted()
                .sorted(key="company_id", reverse=True)
                .sorted(key="country_id", reverse=True)
            )
        else:
            res = self.related_hs_code_ids.filtered(
                lambda hs: (hs.company_id.id in company_ids)
            )
            res = res.sorted(key="company_id", reverse=True)
        if res:
            res = res[0]
        return res
