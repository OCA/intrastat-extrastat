# Copyright 2026 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models

from odoo.addons.account.models.chart_template import template


class AccountChartTemplate(models.AbstractModel):
    _inherit = "account.chart.template"

    @template(model="account.fiscal.position")
    def _get_account_fiscal_position(self, template_code):
        """Define the appropriate value (intrastat=no) as the default value, for
        example when defining a chart of accounts in a company.
        If specific values need to be defined for a chart of accounts, it will be
        necessary to use the _get_fiscal_position() method, as is done in
        l10n_es_intrastat_report.
        """
        res = super()._get_account_fiscal_position(template_code=template_code)
        [v.update({"intrastat": "no"}) for v in res.values()]
        return res
