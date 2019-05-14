import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo11-addons-oca-intrastat-extrastat",
    description="Meta package for oca-intrastat-extrastat Odoo addons",
    version=version,
    install_requires=[
        'odoo11-addon-intrastat_base',
        'odoo11-addon-intrastat_product',
        'odoo11-addon-intrastat_product_generic',
        'odoo11-addon-product_harmonized_system',
        'odoo11-addon-product_harmonized_system_delivery',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
