#  Copyright (c) 2024 Groupe Voltaire
#  @author Emilie SOUTIRAS  <emilie.soutiras@groupevoltaire.com>
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _get_intrastat_lines_info(self):
        destination_country = self.partner_id.country_id or False
        self.env.context = dict(self.env.context)
        self.env.context.update({"hs_code_for_country": destination_country.id})
        res = {}
        for line in (
            self.invoice_line_ids.filtered(
                lambda x: x.product_id.get_hs_code_recursively()
                and x.product_id.origin_country_id
            )
            if not self.intrastat_line_ids
            else self.intrastat_line_ids
        ):
            res.setdefault(line.product_id.id, {"weight": 0})
            vals = self._prepare_intrastat_line_info(line)
            if vals.get("hs_code_id"):
                weight = vals.pop("weight")
                res[line.product_id.id].update(vals)
                res[line.product_id.id]["weight"] += weight
            else:
                res.pop(line.product_id.id)
        # sort res :
        if res:
            res = dict(
                sorted(
                    res.items(), key=lambda val: val[1]["product_id"].display_name or ""
                )
            )
        return res.values()

    def _prepare_intrastat_line_info(self, line):
        res = super()._prepare_intrastat_line_info(line)
        if "hs_code_id" in res:
            res.update({"hs_code_id": line.product_id.get_hs_code_recursively()})
        return res
