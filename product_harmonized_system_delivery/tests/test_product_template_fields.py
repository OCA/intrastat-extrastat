from odoo.addons.base.tests.common import BaseCommon


class TestProductTemplateFields(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.country = cls.env.ref("base.us")
        cls.HS1 = cls.env["hs.code"].create(
            {
                "local_code": "12345678",
                "description": "Test Description",
            }
        )
        cls.product_tmpl = cls.env["product.template"].create(
            {
                "name": "Test Product Template",
                "hs_code_id": cls.HS1.id,
                "origin_country_id": cls.country.id,
            }
        )

        cls.Product = cls.product_tmpl.product_variant_id

    def test_product_template_field_values(self):
        """Verifies that custom fields overwrite Odoo fields"""
        self.assertEqual(
            self.product_tmpl.hs_code,
            self.HS1.hs_code,
            "The HS code did not overwrite the original value as expected.",
        )
        self.assertEqual(
            self.product_tmpl.country_of_origin,
            self.country,
            "The country of origin did not overwrite the original value as expected.",
        )
