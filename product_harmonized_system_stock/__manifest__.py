# Copyright 2019 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Product Harmonized System (menu entry)",
    "version": "13.0.1.0.0",
    "category": "Reporting",
    "license": "AGPL-3",
    "summary": "Adds a menu entry for H.S. codes",
    "author": "Akretion, Odoo Community Association (OCA)",
    "depends": ["product_harmonized_system", "stock"],
    "data": ["views/hs_code_menu.xml"],
    "installable": True,
    "auto_install": True,
}
