# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.intrastat_base.tests.common import IntrastatCommon


class IntrastatProductCommon(IntrastatCommon):
    @classmethod
    def _init_products(cls):
        # Create category - don't init intrastat values, do it in tests
        vals = {
            "name": "Robots",
            "parent_id": cls.category_saleable.id,
        }
        cls.categ_robots = cls.category_obj.create(vals)

        vals = {
            "name": "C3PO",
            "categ_id": cls.categ_robots.id,
            "origin_country_id": cls.env.ref("base.us").id,
            "weight": 300,
            # Computer - C3PO is one of them
            "hs_code_id": cls.hs_code_computer.id,
        }
        cls.product_c3po = cls.product_template_obj.create(vals)

    @classmethod
    def _init_company(cls):
        # Default transport for company is Road
        cls.demo_company.intrastat_transport_id = cls.transport_road

    @classmethod
    def _init_fiscal_position(cls):
        vals = {
            "name": "Intrastat Fiscal Position",
            "intrastat": True,
        }
        cls.position = cls.position_obj.create(vals)

    @classmethod
    def _init_regions(cls):
        # Create Belgium Region
        cls._create_region()

        vals = {
            "code": "DE",
            "name": "Germany",
            "country_id": cls.env.ref("base.de").id,
            "description": "Germany",
        }
        cls._create_region(vals)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.region_obj = cls.env["intrastat.region"]
        cls.transaction_obj = cls.env["intrastat.transaction"]
        cls.transport_mode_obj = cls.env["intrastat.transport_mode"]
        cls.partner_obj = cls.env["res.partner"]
        cls.category_saleable = cls.env.ref("product.product_category_1")
        cls.category_obj = cls.env["product.category"]
        cls.product_template_obj = cls.env["product.template"]
        cls.declaration_obj = cls.env["intrastat.product.declaration"]
        cls.position_obj = cls.env["account.fiscal.position"]
        cls.hs_code_computer = cls.env.ref("product_harmonized_system.84715000")

        cls.transport_rail = cls.env.ref("intrastat_product.intrastat_transport_2")
        cls.transport_road = cls.env.ref("intrastat_product.intrastat_transport_3")

        cls._init_regions()
        cls._init_company()
        cls._init_fiscal_position()
        cls._init_products()

    @classmethod
    def _create_region(cls, vals=None):
        values = {
            "code": "BE_w",
            "country_id": cls.env.ref("base.be").id,
            "company_id": cls.env.company.id,
            "description": "Belgium Walloon Region",
            "name": "Walloon Region",
        }
        if vals is not None:
            values.update(vals)
        cls.region = cls.region_obj.create(values)

    @classmethod
    def _create_transaction(cls, vals=None):
        values = {
            "code": "11",
            "company_id": cls.env.company.id,
            "description": "Sale / Purchase",
        }
        if vals is not None:
            values.update(vals)
        cls.transaction = cls.transaction_obj.create(values)

    @classmethod
    def _create_transport_mode(cls, vals=None):
        values = {}
        if vals is not None:
            values.update(vals)
        cls.transport_mode = cls.transport_mode_obj.create(values)

    @classmethod
    def _create_declaration(cls, vals=None):
        values = {
            "company_id": cls.env.company.id,
            "declaration_type": "dispatches",
        }
        if vals is not None:
            values.update(vals)
        cls.declaration = cls.declaration_obj.create(values)
