{
    "name": "Propagate incoterm from sale delivery to invoice",
    "version": "17.0.1.0.0",
    "category": "Accounting",
    "author": "FactorLibre, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/intrastat-extrastat",
    "license": "AGPL-3",
    "summary": "Propagates the value of the incoterm fields from the order shipping "
    "method to the invoices",
    "depends": [
        "sale_stock",
        "delivery",
        "intrastat_product",
    ],
    "data": ["views/delivery_carrier_view.xml"],
    "installable": True,
    "application": False,
}
