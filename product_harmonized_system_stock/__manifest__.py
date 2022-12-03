# Copyright 2019-2022 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Product Harmonized System (menu entry)",
    "version": "15.0.1.0.0",
    "category": "Reporting",
    "license": "AGPL-3",
    "summary": "Adds a menu entry for H.S. codes",
    "author": "Akretion, Odoo Community Association (OCA)",
    "maintainers": ["alexis-via", "luc-demeyer"],
    "website": "https://github.com/OCA/intrastat-extrastat",
    "depends": ["product_harmonized_system", "stock"],
    "data": ["views/hs_code_menu.xml"],
    "installable": True,
    "auto_install": True,
}
