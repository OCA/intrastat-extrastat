# Copyright 2011-2020 Akretion (http://www.akretion.com)
# Copyright 2018-2020 brain-tec AG (Kumar Aberer <kumar.aberer@braintec-group.com>)
# Copyright 2009-2020 Noviat (http://www.noviat.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Intrastat Reporting Base",
    "version": "14.0.2.1.0",
    "category": "Intrastat",
    "license": "AGPL-3",
    "summary": "Base module for Intrastat reporting",
    "author": "ACSONE SA/NV, Akretion,Noviat,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/intrastat-extrastat",
    "depends": ["base_vat", "account"],
    "excludes": ["account_intrastat"],
    "data": [
        "views/product_template.xml",
        "views/res_partner.xml",
        "views/res_config_settings.xml",
        "views/intrastat.xml",
        "views/account_fiscal_position.xml",
    ],
    "demo": ["demo/intrastat_demo.xml"],
    "installable": True,
}
