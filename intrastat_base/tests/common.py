# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo_test_helper import FakeModelLoader

from odoo.modules.module import get_resource_path
from odoo.tools import convert_file


class IntrastatCommon(object):
    @classmethod
    def _load_xml(cls, module, filepath):
        convert_file(
            cls.env.cr,
            module,
            get_resource_path(module, filepath),
            {},
            mode="init",
            noupdate=False,
            kind="test",
        )

    @classmethod
    def _load_test_declaration(cls):
        cls.loader = FakeModelLoader(cls.env, cls.__module__)
        cls.loader.backup_registry()

        # The fake class is imported here !! After the backup_registry
        from .models import IntrastatDeclarationTest

        cls.loader.update_registry((IntrastatDeclarationTest,))

    @classmethod
    def _create_declaration(cls, vals=None):
        values = {
            "company_id": cls.declaration_test_obj._default_company_id().id,
            "year": "2021",
            "month": "03",
        }
        if vals is not None:
            values.update(vals)
        cls.declaration = cls.declaration_test_obj.create(values)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.chart_template_obj = cls.env["account.chart.template"]
        cls.mail_obj = cls.env["mail.mail"]

        cls.demo_user = cls.env.ref("base.user_demo")
        cls.demo_company = cls.env.ref("base.main_company")

        cls.shipping_cost = cls.env.ref("intrastat_base.shipping_costs_exclude")
        cls._load_test_declaration()
        cls.declaration_test_obj = cls.env["intrastat.declaration.test"]
        cls._load_xml("intrastat_base", "tests/data/mail_template.xml")
        cls.mail_template_id = (
            "intrastat_base.base_intrastat_product_reminder_email_template"
        )

    @classmethod
    def tearDownClass(cls):
        cls.loader.restore_registry()
        super().tearDownClass()
