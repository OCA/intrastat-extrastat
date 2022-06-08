# Copyright 2022 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests import Form, common


class TestIntrastatProduct(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.account_receivable = cls._create_account(cls, "receivable")
        cls.account_payable = cls._create_account(cls, "payable")
        cls.account_income = cls._create_account(cls, "other_income")
        cls.account_expense = cls._create_account(cls, "expenses")
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test product",
                "hs_code_id": cls.env.ref("product_harmonized_system.84715000").id,
                "origin_country_id": cls.env.ref("base.de").id,
                "weight": 1.25,
            }
        )
        cls.partner = cls.env["res.partner"].create(
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

    def _create_account(self, account_type):
        external_id = "account.data_account_type_%s" % account_type
        return self.env["account.account"].create(
            {
                "name": "Test Account (%s)" % account_type,
                "code": "TEST-%s" % account_type,
                "user_type_id": self.env.ref(external_id).id,
                "reconcile": True,
            }
        )

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
        res = self.report_obj._get_report_from_name(
            "account.report_invoice_with_payments"
        ).render_qweb_text(self.invoice.ids, False)
        self.assertRegex(str(res[0]), self.product.hs_code_id.hs_code)
        self.assertRegex(str(res[0]), self.product.origin_country_id.name)
        res = list(self.invoice._get_intrastat_lines_info())
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]["product_id"], self.product)
        self.assertEqual(res[0]["hs_code_id"], self.product.hs_code_id)
        self.assertEqual(res[0]["origin_country_id"], self.product.origin_country_id)
        self.assertEqual(res[0]["weight"], weight)

    def test_invoice_report_without_intrastat_lines(self):
        self._test_invoice_report(2.5)

    def test_invoice_report_with_intrastat_lines(self):
        self.invoice.compute_intrastat_lines()
        self._test_invoice_report(2)
