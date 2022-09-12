import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-oca-intrastat-extrastat",
    description="Meta package for oca-intrastat-extrastat Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-intrastat_base>=15.0dev,<15.1dev',
        'odoo-addon-intrastat_product>=15.0dev,<15.1dev',
        'odoo-addon-product_harmonized_system>=15.0dev,<15.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 15.0',
    ]
)
