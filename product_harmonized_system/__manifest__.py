# -*- coding: utf-8 -*-
# © 2011-2016 Akretion (http://www.akretion.com)
# © 2009-2016 Noviat (http://www.noviat.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# @author Luc de Meyer <info@noviat.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Product Harmonized System Codes',
    'version': '10.0.1.0.0',
    'category': 'Reporting',
    'license': 'AGPL-3',
    'summary': 'Base module for Product Import/Export reports',
    'author': 'Akretion, Noviat, Odoo Community Association (OCA)',
    'depends': ['product'],
    'conflicts': ['report_intrastat'],
    'data': [
        'security/product_hs_security.xml',
        'security/ir.model.access.csv',
        'views/hs_code.xml',
        'views/product_category.xml',
        'views/product_template.xml',
    ],
    'demo': [
        'demo/product_demo.xml',
    ],
    'installable': True,
}
