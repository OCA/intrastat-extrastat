# Copyright 2019-2025 Akretion France (http://www.akretion.com)
# @author Olivier Nibart <olivier.nibart@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "product_harmonized_system_tax_rate",
    "summary": """
        Add a notion of tax rate linked to an H.S. Code and Country.""",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "author": "Akretion, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/intrastat-extrastat",
    "depends": [
        "product_harmonized_system_stock",
    ],
    "maintainers": ["nayatec", "hparfr"],
    "data": [
        "views/hs_code_tax_rate_views.xml",
        "views/hs_code_views.xml",
        "views/product_views.xml",
        "security/ir.model.access.csv",
    ],
}
