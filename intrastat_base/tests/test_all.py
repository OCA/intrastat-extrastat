from odoo.tests.common import TransactionCase


class TestIntrastatBase(TransactionCase):
    """Tests for this module"""

    def test_company(self):
        # add 'Demo user' to intrastat_remind_user_ids
        demo_user = self.env.ref("base.user_demo")
        demo_company = self.env.ref("base.main_company")
        demo_company.write({"intrastat_remind_user_ids": [(6, False, [demo_user.id])]})
        # then check if intrastat_email_list contains the email of the user
        self.assertEqual(demo_company.intrastat_email_list, demo_user.email)
