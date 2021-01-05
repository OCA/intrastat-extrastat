# Copyright 2020 Akretion France (http://www.akretion.com/)
# @author: <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountFiscalPosition(models.Model):
    _inherit = "account.fiscal.position"

    intrastat = fields.Boolean(
        string="Intrastat",
        help="Set to True if the invoices with this fiscal position should "
        "be taken into account for the generation of the intrastat reports.",
    )


class AccountFiscalPositionTemplate(models.Model):
    _inherit = "account.fiscal.position.template"

    intrastat = fields.Boolean(string="Intrastat")


class AccountChartTemplate(models.Model):
    _inherit = "account.chart.template"

    def _get_fp_vals(self, company, position):
        vals = super()._get_fp_vals(company, position)
        vals["intrastat"] = position.intrastat
        return vals
