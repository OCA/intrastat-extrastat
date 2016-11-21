# -*- coding: utf-8 -*-

from openerp.tests.common import TransactionCase


class TestHs(TransactionCase):
    """Tests for unit of measure conversion"""

    def setUp(self):
        super(TestHs, self).setUp()
        self.hs_code = self.env['hs.code']

    def test_10_all_functionality(self):
        # Create HS code
        code1 = self.hs_code.create({
            'local_code': 'TEST 6789'
        })
        # - Test whether code is correctly de-spaced and truncated
        self.assertEquals(code1.hs_code, 'TEST67')

        # For the category 'Saleable':
        category1 = self.env.ref('product.product_category_1')
        # - Set HS code on it
        category1.hs_code_id = code1

        # For the demo category 'Software' (child of Saleable):
        category2 = self.env.ref('product.product_category_4')
        # - Test if the HS code is null
        self.assertFalse(category2.hs_code_id)
        # - Test if the recursive HS code is the one we set on Saleable
        self.assertEquals(category2.get_hs_code_recursively(), code1)

        # For the product 'Windows 7 Professional' (category Software)
        product1 = self.env.ref('product.product_product_40')
        # - Test if the HS code is null
        self.assertFalse(product1.hs_code_id)
        # - Test if the recursive HS code is the one we set on Saleable
        self.assertEquals(
            product1.product_tmpl_id.get_hs_code_recursively(),
            code1)
        # - Set HS code on it
        product1.hs_code_id = code1
        # - Set country to 'us'
        product1.origin_country_id = self.env.ref('base.us')
