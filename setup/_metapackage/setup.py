import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-oca-intrastat-extrastat",
    description="Meta package for oca-intrastat-extrastat Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-intrastat_base',
        'odoo14-addon-intrastat_product',
        'odoo14-addon-intrastat_product_generic',
        'odoo14-addon-product_harmonized_system',
        'odoo14-addon-product_harmonized_system_delivery',
        'odoo14-addon-product_harmonized_system_stock',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
