# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


class IntrastatCommon:
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.chart_template_obj = cls.env["account.chart.template"]
        cls.mail_obj = cls.env["mail.mail"]

        cls.demo_user = cls.env.ref("base.user_demo")
        cls.demo_company = cls.env.ref("base.main_company")

        cls.shipping_cost = cls.env["product.product"].create(
            {
                "name": "Shipping costs TEST",
                "default_code": "TEST_SHIP",
                "type": "service",
                "is_accessory_cost": True,
                "categ_id": cls.env.ref("product.product_category_services"),
            }
        )
