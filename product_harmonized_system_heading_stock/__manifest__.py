# Copyright 2023 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Product Harmonized System Header (menu entry)",
    "version": "13.0.1.0.0",
    "category": "Reporting",
    "license": "AGPL-3",
    "summary": "Adds a Menu Entry for H.S. Code Heading",
    "website": "https://github.com/OCA/intrastat-extrastat",
    "author": "ForgeFlow, Odoo Community Association (OCA)",
    "depends": ["product_harmonized_system_heading", "stock"],
    "data": ["views/hs_code_header_menu.xml"],
    "installable": True,
    "application": False,
    "auto_install": True,
}
