import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo8-addons-oca-intrastat",
    description="Meta package for oca-intrastat Odoo addons",
    version=version,
    install_requires=[
        'odoo8-addon-intrastat_base',
        'odoo8-addon-intrastat_product',
        'odoo8-addon-product_harmonized_system',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
