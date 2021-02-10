# Copyright 2011-2016 Akretion (http://www.akretion.com)
# Copyright 2018 brain-tec AG (Kumar Aberer <kumar.aberer@braintec-group.com>)
# Copyright 2009-2020 Noviat (http://www.noviat.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Intrastat Reporting Base",
    "version": "13.0.1.1.1",
    "category": "Intrastat",
    "license": "AGPL-3",
    "summary": "Base module for Intrastat reporting",
    "author": "Akretion,Noviat,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/intrastat",
    "depends": ["base_vat", "account"],
    "excludes": ["account_intrastat"],
    "data": [
        "data/country_data.xml",
        "views/product_template.xml",
        "views/res_partner.xml",
        "views/res_country.xml",
        "views/account_tax.xml",
        "views/res_config_settings.xml",
        "views/intrastat.xml",
    ],
    "demo": ["demo/intrastat_demo.xml"],
    "installable": True,
}
