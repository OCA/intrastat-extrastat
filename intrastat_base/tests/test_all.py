from odoo.exceptions import ValidationError

from .common import IntrastatCommon


class TestIntrastatBase(IntrastatCommon):
    """Tests for this module"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_company(self):
        # add 'Demo user' to intrastat_remind_user_ids
        self.demo_company.write(
            {"intrastat_remind_user_ids": [(6, False, [self.demo_user.id])]}
        )
        # then check if intrastat_email_list contains the email of the user
        self.assertEqual(self.demo_company.intrastat_email_list, self.demo_user.email)

    def test_no_email(self):
        self.demo_user.email = False
        with self.assertRaises(ValidationError):
            self.demo_company.write(
                {"intrastat_remind_user_ids": [(6, False, [self.demo_user.id])]}
            )

    def test_accessory(self):
        with self.assertRaises(ValidationError):
            self.shipping_cost.type = "consu"

    def test_fiscal_position(self):
        with self.assertRaises(ValidationError):
            self.env["account.fiscal.position"].create(
                {
                    "name": "TestB2B",
                    "vat_required": False,
                    "intrastat": "b2b",
                }
            )
        with self.assertRaises(ValidationError):
            self.env["account.fiscal.position"].create(
                {
                    "name": "TestB2C",
                    "vat_required": True,
                    "intrastat": "b2c",
                }
            )
