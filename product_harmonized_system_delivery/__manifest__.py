# Copyright 2018-2022 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Product Harmonized System Codes - Delivery",
    "version": "15.0.1.0.0",
    "category": "Reporting",
    "license": "AGPL-3",
    "summary": "Hide native hs_code field provided by the delivery module",
    "author": "Akretion, Odoo Community Association (OCA)",
    "maintainers": ["alexis-via", "luc-demeyer"],
    "website": "https://github.com/OCA/intrastat-extrastat",
    "depends": ["delivery", "product_harmonized_system"],
    "data": ["views/product_template.xml"],
    "installable": True,
    "auto_install": True,
}
