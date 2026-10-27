# Copyright 2026 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import Form

from odoo.addons.base.tests.common import BaseCommon


class TestHSCode(BaseCommon):
    _test_user_groups = ("base.group_system", "product.group_product_manager")

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(user=cls._test_user)
        cls.parent_categ = cls.env["product.category"].create({"name": "Parent"})
        cls.categ = cls.env["product.category"].create(
            {"name": "Child", "parent_id": cls.parent_categ.id}
        )
        cls.product = cls.env["product.product"].create(
            {"name": "Test product", "categ_id": cls.categ.id}
        )

    def _create_hs_code(self, local_code, description):
        with Form(self.env["hs.code"]) as hs_form:
            hs_form.local_code = local_code
            hs_form.description = description
        return hs_form.record

    def test_hs_code_from_local_code(self):
        hs_code = self._create_hs_code("8471 30 00", "Portable computers")
        self.assertEqual(hs_code.local_code, "84713000")
        self.assertEqual(hs_code.hs_code, "847130")
        self.assertEqual(hs_code.display_name, "84713000 Portable computers")
        hs_code.local_code = "8471 41 00"
        self.assertEqual(hs_code.local_code, "84714100")
        self.assertEqual(hs_code.hs_code, "847141")

    def test_hs_code_on_product_and_categories(self):
        parent_code = self._create_hs_code("84713000", "Portable computers")
        product_code = self._create_hs_code("84714100", "Other computers")
        self.assertFalse(self.product.get_hs_code_recursively())
        # Set on the parent category, it is found from the product
        self.parent_categ.hs_code_id = parent_code
        self.assertEqual(self.product.get_hs_code_recursively(), parent_code)
        self.assertEqual(parent_code.product_categ_count, 1)
        # The code of the product itself wins
        with Form(self.product.product_tmpl_id) as tmpl_form:
            tmpl_form.hs_code_id = product_code
        self.assertEqual(self.product.get_hs_code_recursively(), product_code)
        self.assertEqual(product_code.product_tmpl_count, 1)
        self.assertEqual(parent_code.product_tmpl_count, 0)
