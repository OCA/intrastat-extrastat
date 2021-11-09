# Copyright 2009-2020 Noviat.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Generic Intrastat Product Declaration",
    "version": "14.0.1.0.0",
    "category": "Accounting & Finance",
    "website": "https://github.com/OCA/intrastat-extrastat",
    "author": "Noviat," "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["intrastat_product"],
    "data": ["security/intrastat_security.xml", "views/intrastat_product.xml"],
}
