# Copyright 2020 Akretion France (http://www.akretion.com/)
# @author: <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models


class AccountChartTemplate(models.Model):
    _inherit = "account.chart.template"

    def _get_fp_vals(self, company, position):
        """
        Get fiscal position chart template instrastat value
        to create fiscal position
        """
        vals = super()._get_fp_vals(company, position)
        vals["intrastat"] = position.intrastat
        return vals
