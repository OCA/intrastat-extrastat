import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo13-addons-oca-intrastat-extrastat",
    description="Meta package for oca-intrastat-extrastat Odoo addons",
    version=version,
    install_requires=[
        'odoo13-addon-hs_code_link',
        'odoo13-addon-intrastat_base',
        'odoo13-addon-intrastat_product',
        'odoo13-addon-intrastat_product_generic',
        'odoo13-addon-product_harmonized_system',
        'odoo13-addon-product_harmonized_system_delivery',
        'odoo13-addon-product_harmonized_system_stock',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 13.0',
    ]
)
