# Copyright 2011-2017 Akretion (http://www.akretion.com)
# Copyright 2009-2019 Noviat (http://www.noviat.com)
# Copyright 2018 brain-tec AG (http://www.braintec-group.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# @author Luc de Meyer <info@noviat.com>
# @author Kumar Aberer <kumar.aberer@braintec-group.com>

{
    'name': 'Intrastat Product',
    'version': '12.0.1.0.3',
    'category': 'Intrastat',
    'license': 'AGPL-3',
    'summary': 'Base module for Intrastat Product',
    'author': 'brain-tec AG, Akretion, Noviat, '
              'Odoo Community Association (OCA)',
    'depends': [
        'intrastat_base',
        'product_harmonized_system',
        'sale_stock',
        'purchase_stock',
        'report_xlsx_helper',
    ],
    'excludes': ['account_intrastat'],
    'data': [
        'views/hs_code.xml',
        'views/intrastat_region.xml',
        'views/intrastat_unit.xml',
        'views/intrastat_transaction.xml',
        'views/intrastat_transport_mode.xml',
        'views/intrastat_product_declaration.xml',
        'views/res_config_settings.xml',
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
