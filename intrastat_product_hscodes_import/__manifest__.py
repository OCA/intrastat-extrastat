# Copyright 2009-2023 Noviat (http://www.noviat.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Intrastat Product - HS Codes Import",
    "version": "16.0.1.0.0",
    "category": "Intrastat",
    "license": "AGPL-3",
    "summary": "Module used to import HS Codes for Intrastat Product",
    "author": "Noviat, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/intrastat-extrastat",
    "depends": [
        "intrastat_product",
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizards/intrastat_hscodes_import_installer_views.xml",
    ],
    "installable": True,
}
