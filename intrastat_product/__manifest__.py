# Copyright 2011-2020 Akretion (http://www.akretion.com)
# Copyright 2009-2020 Noviat (http://www.noviat.com)
# Copyright 2018-2020 brain-tec AG (http://www.braintec-group.com)
# Copyright 2022 Tecnativa - Víctor Martínez
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# @author Luc de Meyer <info@noviat.com>
# @author Kumar Aberer <kumar.aberer@braintec-group.com>

{
    "name": "Intrastat Product",
    "version": "15.0.1.0.2",
    "category": "Intrastat",
    "license": "AGPL-3",
    "summary": "Base module for Intrastat Product",
    "author": "ACSONE SA/NV, brain-tec AG, Akretion, Noviat, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/intrastat-extrastat",
    "depends": [
        "intrastat_base",
        "product_harmonized_system",
        "sale_stock",
        "purchase_stock",
        "report_xlsx_helper",
    ],
    "excludes": ["account_intrastat"],
    "external_dependencies": {"python": ["python-stdnum>=1.16"]},
    "data": [
        "security/intrastat_security.xml",
        "security/ir.model.access.csv",
        "views/hs_code.xml",
        "views/intrastat_region.xml",
        "views/intrastat_unit.xml",
        "views/intrastat_transaction.xml",
        "views/intrastat_transport_mode.xml",
        "views/intrastat_product_declaration.xml",
        "views/res_config_settings.xml",
        "views/res_partner_view.xml",
        "views/account_move.xml",
        "views/sale_order.xml",
        "views/stock_warehouse.xml",
        "views/report_invoice.xml",
        "wizards/intrastat_result_view.xml",
        "data/intrastat_transport_mode.xml",
        "data/intrastat_unit.xml",
    ],
    "demo": ["demo/intrastat_demo.xml"],
    "installable": True,
    "pre_init_hook": "pre_init_hook",
}
