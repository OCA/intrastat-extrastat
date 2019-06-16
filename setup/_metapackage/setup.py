import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo12-addons-oca-intrastat-extrastat",
    description="Meta package for oca-intrastat-extrastat Odoo addons",
    version=version,
    install_requires=[
        'odoo12-addon-intrastat_base',
        'odoo12-addon-intrastat_product',
        'odoo12-addon-intrastat_product_generic',
        'odoo12-addon-product_harmonized_system',
        'odoo12-addon-product_harmonized_system_delivery',
        'odoo12-addon-product_harmonized_system_stock',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
