#  Copyright (c) 2024 Groupe Voltaire
#  @author Emilie SOUTIRAS  <emilie.soutiras@groupevoltaire.com>
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests import TransactionCase

from odoo.addons.intrastat_product.tests.common import IntrastatProductCommon


class TestHSCodes(IntrastatProductCommon, TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.pdt_c3po = cls.product_c3po.product_variant_ids[0]

    def test_hs_code_ids_product(self):
        hs_code_7050 = self.env.ref("product_harmonized_system.84717050")
        self.categ_robots.hs_code_ids = [(4, hs_code_7050.id)]
        self.assertEqual(
            self.pdt_c3po.get_hs_code_recursively(),
            self.hs_code_computer,
        )
        country_fr = self.env.ref("base.fr")
        hs_code_7050.country_id = country_fr
        self.pdt_c3po.hs_code_ids = [
            (4, self.hs_code_computer.id, 0),
            (4, hs_code_7050.id, 0),
        ]
        self.assertEqual(
            self.pdt_c3po.get_hs_code_recursively(),
            self.hs_code_computer,
        )
        self.assertEqual(
            self.pdt_c3po.with_context(
                hs_code_for_country=country_fr.id
            ).get_hs_code_recursively(),
            hs_code_7050,
        )

    def test_hs_code_ids_category(self):
        self.pdt_c3po.hs_code_id = False
        country_fr = self.env.ref("base.fr")
        hs_code_7050 = self.env.ref("product_harmonized_system.84717050")
        hs_code_7050.country_id = country_fr
        hs_code_7049 = hs_code_7050.copy({"local_code": "84717049"})
        self.assertFalse(self.hs_code_computer.country_id)
        self.categ_robots.hs_code_ids = [
            (4, self.hs_code_computer.id, 0),
            (4, hs_code_7050.id, 0),
            (4, hs_code_7049.id, 0),
        ]
        self.assertEqual(
            self.pdt_c3po.categ_id,
            self.categ_robots,
        )
        self.assertEqual(
            self.pdt_c3po.get_hs_code_recursively(),
            self.hs_code_computer,
        )
        self.assertEqual(
            self.pdt_c3po.with_context(
                hs_code_for_country=country_fr.id
            ).get_hs_code_recursively(),
            hs_code_7049,
        )
