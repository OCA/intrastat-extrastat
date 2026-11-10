# Copyright 2026 Akretion (https://www.akretion.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from lxml import html

from odoo import Command
from odoo.tests import new_test_user, tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestInvoiceReport(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.hs_code = cls.env["hs.code"].create(
            {"local_code": "84713000", "description": "Laptops"}
        )
        cls.product_a.write(
            {
                "hs_code_id": cls.hs_code.id,
                "origin_country_id": cls.env.ref("base.cn").id,
            }
        )
        cls.fiscal_position = cls.env["account.fiscal.position"].create(
            {"name": "EU B2B", "display_hscode": True}
        )
        cls.partner_a.invoice_intrastat_detail = True
        cls.invoice = cls.init_invoice(
            "out_invoice", products=cls.product_a, post=False
        )
        cls.invoice.write(
            {
                "fiscal_position_id": cls.fiscal_position.id,
                "invoice_line_ids": [
                    Command.create({"display_type": "line_note", "name": "A note"}),
                    Command.create(
                        {"name": "Service without product", "price_unit": 10}
                    ),
                ],
            }
        )
        cls.invoice_user = new_test_user(
            cls.env, login="invoice_user", groups="account.group_account_invoice"
        )

    def _render_invoice(self):
        content, _ = (
            self.env["ir.actions.report"]
            .with_user(self.invoice_user)
            ._render_qweb_html("account.account_invoices", self.invoice.ids)
        )
        return html.fromstring(content)

    def _line_table(self, document):
        return document.xpath("//table[@name='invoice_line_table']")[0]

    def _header_labels(self, table):
        return [th.text_content().strip() for th in table.xpath(".//thead//th")]

    def _cell_text(self, row, name):
        return row.xpath(f"./td[@name='{name}']")[0].text_content().strip()

    def _product_row(self, table):
        return table.xpath(".//td[@name='td_hs_code']/..")[0]

    def test_hs_code_columns_displayed(self):
        table = self._line_table(self._render_invoice())
        self.assertEqual(self._header_labels(table)[1:3], ["HS Code", "Country"])
        product_row = self._product_row(table)
        self.assertEqual(self._cell_text(product_row, "td_hs_code"), "84713000")
        self.assertEqual(self._cell_text(product_row, "td_origin_country"), "China")

    def test_hs_code_from_product_category(self):
        self.product_a.categ_id.hs_code_id = self.hs_code
        self.product_a.hs_code_id = False
        table = self._line_table(self._render_invoice())
        self.assertEqual(
            self._cell_text(self._product_row(table), "td_hs_code"), "84713000"
        )

    def test_columns_aligned_on_line_without_product(self):
        table = self._line_table(self._render_invoice())
        header_count = len(self._header_labels(table))
        rows = table.xpath(".//tbody/tr[td[@name='td_quantity']]")
        self.assertEqual(len(rows), 2)
        for row in rows:
            self.assertEqual(len(row.xpath("./td")), header_count)

    def test_hs_code_columns_hidden(self):
        self.fiscal_position.display_hscode = False
        table = self._line_table(self._render_invoice())
        self.assertNotIn("HS Code", self._header_labels(table))
        self.assertFalse(table.xpath(".//td[@name='td_hs_code']"))

    def test_intrastat_detail_table_hidden(self):
        document = self._render_invoice()
        self.assertFalse(
            document.xpath("//table[@name='intrastat_transaction_detail']")
        )

    def test_intrastat_detail_table_kept_without_hs_code_columns(self):
        self.fiscal_position.display_hscode = False
        document = self._render_invoice()
        self.assertTrue(document.xpath("//table[@name='intrastat_transaction_detail']"))
