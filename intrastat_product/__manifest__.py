# -*- coding: utf-8 -*-
# © 2011-2017 Akretion (http://www.akretion.com)
# © 2009-2018 Noviat (http://www.noviat.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# @author Luc de Meyer <info@noviat.com>

{
    'name': 'Intrastat Product',
    'version': '10.0.1.3.0',
    'category': 'Intrastat',
    'license': 'AGPL-3',
    'summary': 'Base module for Intrastat Product',
    'author': 'Akretion, Noviat, Odoo Community Association (OCA)',
    'depends': [
        'intrastat_base',
        'product_harmonized_system',
        'sale_stock',
        'purchase',
        'report_xlsx_helper',
        ],
    'conflicts': ['report_intrastat'],
    'data': [
        'views/hs_code.xml',
        'views/intrastat_region.xml',
        'views/intrastat_unit.xml',
        'views/intrastat_transaction.xml',
        'views/intrastat_transport_mode.xml',
        'views/intrastat_product_declaration.xml',
        'views/account_config_settings.xml',
        'views/account_invoice.xml',
        'views/sale_order.xml',
        'views/stock_warehouse.xml',
        'security/intrastat_security.xml',
        'security/ir.model.access.csv',
        'data/intrastat_transport_mode.xml',
        'data/intrastat_unit.xml',
    ],
    'demo': ['demo/intrastat_demo.xml'],
    'installable': True,
}
