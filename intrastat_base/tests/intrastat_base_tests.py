# -*- coding: utf-8 -*-

from openerp.tests.common import TransactionCase

class TestIntrastatBase(TransactionCase):
    """Tests for this module"""

    def setUp(self):
        super(TestIntrastatBase, self).setUp()


    def test_10_countries(self):
        # check if only EU countries have the 'intrastat' bit set
        france = self.env.ref('base.fr')
        self.assertTrue(france.intrastat)
        brazil = self.env.ref('base.br')
        self.assertFalse(brazil.intrastat)
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


    def test_exclude_intrastat(self):
        # Test if exclude_from_intrastat_if_present is false
        exclude_tax = self.env['account.tax'].search([('id', '=', 1)])
        for item in exclude_tax:
            self.assertFalse(item.exclude_from_intrastat_if_present)

    def test_accessory_cost(self):
        accessory_cost = self.env['product.product'].search([('id', '=', 1)])
        for test in accessory_cost:
            self.assertFalse(test.is_accessory_cost)









