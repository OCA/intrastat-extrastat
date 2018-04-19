import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo9-addons-oca-intrastat",
    description="Meta package for oca-intrastat Odoo addons",
    version=version,
    install_requires=[
        'odoo9-addon-intrastat_base',
        'odoo9-addon-product_harmonized_system',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
