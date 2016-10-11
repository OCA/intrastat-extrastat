# -*- coding: utf-8 -*-
# © 2011-2016 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Intrastat Reporting Base',
    'version': '10.0.1.0.0',
    'category': 'Intrastat',
    'license': 'AGPL-3',
    'summary': 'Base module for Intrastat reporting',
    'author': 'Akretion,Odoo Community Association (OCA)',
    'website': 'http://www.akretion.com',
    'depends': ['base_vat'],
    'conflicts': ['report_intrastat'],
    'data': [
        'data/country_data.xml',
        'views/product_template.xml',
        'views/res_partner.xml',
        'views/res_country.xml',
        'views/account_tax.xml',
        'views/account_config_settings.xml',
        'views/intrastat.xml',
    ],
    'demo': [
        'demo/intrastat_demo.xml',
    ],
    'installable': True,
}
