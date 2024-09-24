#  Copyright (c) 2024 Groupe Voltaire
#  @author Emilie SOUTIRAS  <emilie.soutiras@groupevoltaire.com>
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests import TransactionCase
from odoo.tests.common import Form

from odoo.addons.intrastat_product.tests.common import IntrastatProductCommon


class TestHSCodes(IntrastatProductCommon, TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.pdt_c3po = cls.product_c3po.product_variant_ids[0]

    def test_hs_code_ids_product(self):
        hs_code_7050 = self.env.ref("product_harmonized_system.84717050")
        self.categ_robots.hs_code_id = hs_code_7050.id
        self.assertEqual(
            self.pdt_c3po.get_hs_code_recursively(),
            self.hs_code_computer,
        )
        country_fr = self.env.ref("base.fr")
        hs_code_7050.country_id = country_fr
        hs_code_7050.parent_id = self.hs_code_computer
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
        self.categ_robots.hs_code_id = self.hs_code_computer
        hs_code_7050 = self.env.ref("product_harmonized_system.84717050")
        hs_code_7050.country_id = country_fr
        hs_code_7049 = hs_code_7050.copy({"local_code": "84717049"})
        self.assertFalse(self.hs_code_computer.country_id)
        hs_code_7050.parent_id = self.hs_code_computer
        hs_code_7049.parent_id = self.hs_code_computer
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


class TestInvoiceReportHSCode(IntrastatProductCommon, TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.hs_code_84715 = cls.env.ref("product_harmonized_system.84715000")
        cls.hs_code_7050 = cls.env.ref("product_harmonized_system.84717050")
        cls.hs_code_7050.parent_id = cls.hs_code_84715
        cls.hs_code_7050.country_id = cls.env.ref("base.fr")
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test product",
                "hs_code_id": cls.hs_code_84715.id,
                "origin_country_id": cls.env.ref("base.de").id,
                "weight": 1.25,
            }
        )
        cls.partner = cls.partner_obj.create(
            {
                "name": "Test partner",
                "country_id": cls.env.ref("base.fr").id,
                "invoice_intrastat_detail": True,
            }
        )
        cls.env["account.journal"].create(
            {"name": "Test sale journal", "type": "sale", "code": "TEST-sale"}
        )
        cls.report_obj = cls.env["ir.actions.report"]
        cls.sale_order = cls._create_sale_order(cls)
        cls.sale_order.action_confirm()
        cls.sale_order.order_line.qty_delivered = 1
        cls.invoice = cls.sale_order._create_invoices()

    def _create_sale_order(self):
        order_form = Form(self.env["sale.order"])
        order_form.partner_id = self.partner
        with order_form.order_line.new() as line_form:
            line_form.product_id = self.product
        with order_form.order_line.new() as line_form:
            line_form.product_id = self.product
        return order_form.save()

    def _test_invoice_report(self, weight):
        """We need to check weight because if intrastat_line_ids already exist
        the weight will be different because weight field in model is integer."""
        res = self.report_obj._render(
            "account.report_invoice_with_payments", self.invoice.ids
        )
        self.assertRegex(str(res[0]), self.hs_code_7050.hs_code)
        self.assertRegex(str(res[0]), self.product.origin_country_id.name)
        res = list(self.invoice._get_intrastat_lines_info())
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]["product_id"], self.product)
        self.assertNotEqual(res[0]["hs_code_id"], self.product.hs_code_id)
        self.assertEqual(res[0]["hs_code_id"], self.hs_code_7050)
        self.assertEqual(res[0]["origin_country_id"], self.product.origin_country_id)
        self.assertEqual(res[0]["weight"], weight)

    def test_invoice_report_hs_codes(self):
        self.assertTrue(self.sale_order)
        self.assertTrue(self.invoice)
        self.invoice.compute_intrastat_lines()
        self._test_invoice_report(2)
