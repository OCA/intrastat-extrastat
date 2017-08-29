# -*- coding: utf-8 -*-
# Copyright 2011-2017 Akretion (http://www.akretion.com)
# Copyright 2009-2017 Noviat
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Intrastat Product',
    'version': '8.0.1.5.0',
    'category': 'Intrastat',
    'license': 'AGPL-3',
    'summary': 'Base module for Intrastat Product',
    'author': 'Akretion, Noviat, Odoo Community Association (OCA)',
    'depends': [
        'intrastat_base',
        'product_harmonized_system',
        'stock_picking_invoice_link',
        'sale_stock',
        'purchase',
    ],
    'conflicts': ['report_intrastat'],
    'data': [
        'views/hs_code.xml',
        'views/intrastat_region.xml',
        'views/intrastat_unit.xml',
        'views/intrastat_transaction.xml',
        'views/intrastat_transport_mode.xml',
        'views/intrastat_product_declaration.xml',
        'views/res_company.xml',
        'views/account_invoice.xml',
        'views/stock_picking.xml',
        'views/stock_warehouse.xml',
        'security/intrastat_security.xml',
        'security/ir.model.access.csv',
        'data/intrastat_transport_mode.xml',
        'data/intrastat_unit.xml',
    ],
    'demo': ['demo/intrastat_demo.xml'],
    'installable': True,
}
