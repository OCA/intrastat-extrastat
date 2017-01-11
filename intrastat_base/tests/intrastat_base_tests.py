# -*- coding: utf-8 -*-
# © 2016 Sunflower IT (http://sunflowerweb.nl).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests.common import TransactionCase

class TestIntrastatBase(TransactionCase):
    """Tests for this module"""

    def test_10_countries(self):
        # check if only EU countries have the 'intrastat' bit set
        denmark = self.env.ref('base.dk')
        self.assertTrue(denmark.intrastat)
        kenya = self.env.ref('base.ke')
        self.assertFalse(kenya.intrastat)

    def test_20_company(self):
        # add 'Demo user' to intrastat_remind_user_ids
        demo_user = self.env.ref('base.user_demo')
        demo_company = self.env.ref('base.main_company')
        demo_company.write({
            'intrastat_remind_user_ids': [(6, False, [demo_user.id])]
        })
        # then check if intrastat_email_list contains the email of the user
        self.assertEquals(demo_company.intrastat_email_list, demo_user.email)
