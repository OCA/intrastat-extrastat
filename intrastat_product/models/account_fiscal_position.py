# Copyright 2022 Akretion France (http://www.akretion.com/)
# @author: <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountFiscalPosition(models.Model):
    _inherit = "account.fiscal.position"

    intrastat_out_invoice_transaction_id = fields.Many2one(
        comodel_name="intrastat.transaction",
        string="Default Intrastat Transaction For Customer Invoice",
        help="Odoo uses the intrastat transaction of the invoice. "
        "If not set, Odoo uses the default intrastat transaction of "
        "the fiscal position of the invoice. "
        "If not set, Odoo uses the default intrastat transaction of the company.",
    )
    intrastat_out_refund_transaction_id = fields.Many2one(
        comodel_name="intrastat.transaction",
        string="Default Intrastat Transaction for Customer Refunds",
        help="Odoo uses the intrastat transaction of the invoice. "
        "If not set, Odoo uses the default intrastat transaction of "
        "the fiscal position of the invoice. "
        "If not set, Odoo uses the default intrastat transaction of the company.",
    )
    intrastat_in_invoice_transaction_id = fields.Many2one(
        comodel_name="intrastat.transaction",
        string="Default Intrastat Transaction For Supplier Invoices",
        help="Odoo uses the intrastat transaction of the invoice. "
        "If not set, Odoo uses the default intrastat transaction of "
        "the fiscal position of the invoice. "
        "If not set, Odoo uses the default intrastat transaction of the company.",
    )
    intrastat_in_refund_transaction_id = fields.Many2one(
        comodel_name="intrastat.transaction",
        string="Default Intrastat Transaction For Supplier Refunds",
        help="Odoo uses the intrastat transaction of the invoice. "
        "If not set, Odoo uses the default intrastat transaction of "
        "the fiscal position of the invoice. "
        "If not set, Odoo uses the default intrastat transaction of the company.",
    )
    # field used to show/hide fields in country-specific modules
    company_country_code = fields.Char(related="company_id.country_id.code")
