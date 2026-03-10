# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import new_test_user

from odoo.addons.base.tests.common import BaseCommon


class IntrastatCommon(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.chart_template_obj = cls.env["account.chart.template"]
        cls.mail_obj = cls.env["mail.mail"]

        cls.demo_user = new_test_user(
            cls.env,
            login="test-user",
            email="test@test.com",
        )
        cls.demo_company = cls.company

        cls.shipping_cost = cls.env["product.product"].create(
            {
                "name": "Shipping costs TEST",
                "default_code": "TEST_SHIP",
                "type": "service",
                "is_accessory_cost": True,
                "categ_id": cls.env.ref("product.product_category_services").id,
            }
        )
