# Copyright 2023 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.exceptions import ValidationError
from odoo.tests.common import SavepointCase


class TestProductHarmonizedSystemHeading(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Models
        cls.hs_code_model = cls.env["hs.code"]
        cls.hs_code_heading_model = cls.env["hs.code.heading"]

    @classmethod
    def _create_hs_code_heading(cls, code="1234", description=False):
        return cls.hs_code_heading_model.create(
            {"code": code, "description": description}
        )

    @classmethod
    def _create_hs_code(cls, local_code="123456789", heading=False, description=False):
        return cls.hs_code_model.create(
            {
                "local_code": local_code,
                "hs_code_heading_id": heading.id if heading else False,
                "description": description,
            }
        )

    def test_01_check_create_hs_code_with_no_heading(self):
        """
        Check that a Heading is automatically created if there is none for the H.S.
        Code.
        """
        local_code = "123456789"
        heading_code = local_code[:4]
        self._create_hs_code(local_code=local_code)
        heading = self.hs_code_heading_model.search(
            [("code", "=", heading_code)], limit=1
        )
        self.assertTrue(heading)

    def test_02_check_hs_code_creation(self):
        """
        Check that the H.S. Code is correctly created if there is a related Heading.
        """
        heading = self._create_hs_code_heading(code="5678")
        code = self._create_hs_code(local_code="56789123", heading=heading)
        self.assertTrue(code)

    def test_03_check_hs_code_creation(self):
        """
        Check that a ValidationError is raised if the H.S. Local Code has less than 4
        digits.
        """
        with self.assertRaises(ValidationError):
            self._create_hs_code(local_code="123")

    def test_04_check_correct_hs_code_name_get_value(self):
        """
        Check that the H.S. Code display name is correctly set based on the changes.
        """
        heading_description = "Heading Description"
        code_description = "Code Description"
        heading = self._create_hs_code_heading(description=heading_description)
        code = self._create_hs_code(heading=heading, description=code_description)
        self.assertEqual(
            code.name_get()[0][1],
            "123456789 %s: %s" % (heading_description, code_description),
        )

    def test_05_check_correct_hs_code_heading_name_get_value(self):
        """
        Check that the H.S. Code display name is correctly set based on the changes.
        """
        heading_description = "Heading Description 2"
        heading = self._create_hs_code_heading(description=heading_description)
        self.assertEqual(heading.name_get()[0][1], "1234 %s" % heading_description)
