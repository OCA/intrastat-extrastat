# Copyright 2023 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Product Harmonized System Code Heading",
    "summary": """
        Adds a heading model for the Product Harmonized System Codes (H.S. Codes).
    """,
    "version": "13.0.1.0.0",
    "category": "Reporting",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/intrastat-extrastat",
    "author": "ForgeFlow, Odoo Community Association (OCA)",
    "depends": ["product_harmonized_system"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/hs_code_heading_views.xml",
        "views/hs_code_views.xml",
    ],
    "maintainers": ["GuillemCForgeFlow"],
    "installable": True,
    "application": False,
    "post_init_hook": "post_init_hook",
}
