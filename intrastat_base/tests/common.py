# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.base.tests.common import BaseCommon


class IntrastatCommon(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.chart_template_obj = cls.env["account.chart.template"]
        cls.mail_obj = cls.env["mail.mail"]

        cls.demo_user = cls.env.ref("base.user_demo")
        cls.demo_company = cls.env.ref("base.main_company")

        cls.shipping_cost = cls.env.ref("intrastat_base.shipping_costs_exclude")
