# Copyright 2025 Akretion (https://www.akretion.com).
# @author Mathieu Delva <mathieu.delva@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Intrastat product hs_code report_line",
    "summary": "alternative to the basic view of the intrastat module",
    "version": "14.0.1.1.0",
    "author": "Akretion, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/intrastat-extrastat",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["account", "intrastat_product"],
    "data": [
        "report/invoice_report.xml",
        "views/account_fiscal_position.xml",
    ],
}
