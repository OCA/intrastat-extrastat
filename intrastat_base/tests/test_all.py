from odoo.exceptions import UserError, ValidationError
from odoo.tests.common import SavepointCase

from .common import IntrastatCommon


class TestIntrastatBase(IntrastatCommon):
    """Tests for this module"""

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

    def test_declaration_no_country(self):
        self.demo_company.country_id = False
        with self.assertRaises(ValidationError):
            self._create_declaration()
            self.declaration.flush()

    def test_declaration_no_vat(self):
        self.demo_company.partner_id.vat = False
        with self.assertRaises(UserError):
            self._create_declaration()
            self.declaration.flush()
            self.declaration._check_generate_xml()

    def test_declaration_send_mail(self):
        self._create_declaration()
        mail_before = self.mail_obj.search([])
        self.declaration.send_reminder_email(self.mail_template_id)
        mail_after = self.mail_obj.search([]) - mail_before
        self.assertEqual(0, len(mail_after))
        self.demo_company.write(
            {"intrastat_remind_user_ids": [(6, False, [self.demo_user.id])]}
        )
        self.declaration.send_reminder_email(self.mail_template_id)
        mail_after = self.mail_obj.search([]) - mail_before
        self.assertEqual(1, len(mail_after))
        self.assertIn(
            mail_after.email_to,
            self.demo_user.email,
        )

    def test_declaration_state(self):
        self._create_declaration()
        self.declaration.unlink()

        self._create_declaration()
        self.declaration.state = "done"
        with self.assertRaises(UserError):
            self.declaration.unlink()


class TestIntrastat(TestIntrastatBase, SavepointCase):
    """ Test Intrastat """
