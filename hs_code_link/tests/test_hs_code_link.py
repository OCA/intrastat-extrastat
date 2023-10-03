# Copyright 2023 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests.common import SavepointCase


class TestHSCodeLink(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Models
        cls.company_model = cls.env["res.company"]
        cls.hs_code_model = cls.env["hs.code"]
        cls.product_template_model = cls.env["product.template"]
        cls.property_model = cls.env["ir.property"]

        # Instances
        cls.company_1 = cls._create_company("Company 1")
        cls.company_2 = cls._create_company("Company 2")

        cls.hs_code_1 = cls._create_hs_code()
        cls.hs_code_2 = cls._create_hs_code("12345678910")

        cls.product_template = cls._create_product_template("Product Template 1")

    @classmethod
    def _create_company(cls, name):
        return cls.company_model.create({"name": name})

    @classmethod
    def _create_hs_code(cls, local_code="123456789", description=False):
        return cls.hs_code_model.create(
            {"local_code": local_code, "description": description}
        )

    @classmethod
    def _create_product_template(cls, name):
        return cls.product_template_model.create({"name": name})

    def test_01_check_correctly_sync_values_in_different_companies(self):
        """
        Check that the values are correctly synced in different companies.
        """
        # First Company
        template_company_1 = self.product_template.with_context(
            force_company=self.company_1.id
        )
        template_company_1.hs_code_id = self.hs_code_1
        self.assertEqual(
            template_company_1.hs_code,
            self.hs_code_1.hs_code,
            "The H.S. Codes should be the same.",
        )
        # Second Company
        template_company_2 = self.product_template.with_context(
            force_company=self.company_2.id
        )
        template_company_2.hs_code_id = self.hs_code_2
        self.assertEqual(
            template_company_2.hs_code,
            self.hs_code_2.hs_code,
            "The H.S. Codes should be the same.",
        )
