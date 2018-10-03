import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo10-addons-oca-intrastat",
    description="Meta package for oca-intrastat Odoo addons",
    version=version,
    install_requires=[
        'odoo10-addon-hs_code_link',
        'odoo10-addon-intrastat_base',
        'odoo10-addon-intrastat_product',
        'odoo10-addon-intrastat_product_generic',
        'odoo10-addon-product_harmonized_system',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
