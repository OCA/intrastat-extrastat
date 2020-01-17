# Copyright 2011-2019 Akretion France (http://www.akretion.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountTax(models.Model):
    _inherit = "account.tax"

    exclude_from_intrastat_if_present = fields.Boolean(
        string="Exclude invoice line from intrastat if this tax is present",
        help="If this tax is present on an invoice line, this invoice "
        "line will be skipped when generating Intrastat Product or "
        "Service lines from invoices.",
    )


class AccountTaxTemplate(models.Model):
    _inherit = "account.tax.template"

    exclude_from_intrastat_if_present = fields.Boolean(
        string="Exclude invoice line from intrastat if this tax is present",
        help="If this tax is present on an invoice line, this invoice "
        "line will be skipped when generating Intrastat Product or "
        "Service lines from invoices.",
    )
