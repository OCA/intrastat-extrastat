import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-oca-intrastat-extrastat",
    description="Meta package for oca-intrastat-extrastat Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-product_harmonized_system>=16.0dev,<16.1dev',
        'odoo-addon-product_harmonized_system_delivery>=16.0dev,<16.1dev',
        'odoo-addon-product_harmonized_system_stock>=16.0dev,<16.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 16.0',
    ]
)
