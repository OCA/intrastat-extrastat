# © 2023 FactorLibre - Luis J. Salvatierra <luis.salvatierra@factorlibre.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields
from odoo.tests.common import tagged

from .common_purchase import IntrastatPurchaseCommon
from .common_sale import IntrastatSaleCommon


@tagged("post_install", "-at_install")
class TestIntrastatAccountMoveReversal(IntrastatSaleCommon, IntrastatPurchaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.tr_11 = cls.env.ref("intrastat_product.intrastat_transaction_11")
        cls.tr_12 = cls.env.ref("intrastat_product.intrastat_transaction_12")
        cls.tr_21 = cls.env.ref("intrastat_product.intrastat_transaction_21")
        cls.incoterm = cls.env["account.incoterms"].create(
            {
                "name": "Test Incoterm",
                "code": "TEST",
            }
        )

    def _create_out_invoice(self):
        self._create_sale_order()
        self.sale.action_confirm()
        self.sale.picking_ids.action_assign()
        for line in self.sale.picking_ids.move_line_ids:
            line.qty_done = line.reserved_uom_qty
        self.sale.picking_ids._action_done()
        self.assertEqual("done", self.sale.picking_ids.state)
        return self.sale._create_invoices()

    def _create_in_invoice(self):
        self._create_purchase_order()
        self.purchase.button_confirm()
        self.purchase.picking_ids.action_assign()
        for line in self.purchase.picking_ids.move_line_ids:
            line.qty_done = line.reserved_uom_qty
        self.purchase.picking_ids._action_done()
        self.assertEqual("done", self.purchase.picking_ids.state)
        action = self.purchase.action_create_invoice()
        invoice_id = action["res_id"]
        return self.move_obj.browse(invoice_id)

    def test_out_invoice_reversal(self):
        date_order = "2021-09-01"
        invoice = self._create_out_invoice()
        invoice.invoice_date = fields.Date.from_string(date_order)
        invoice.intrastat_fiscal_position = "b2c"
        invoice.action_post()
        self.assertFalse(invoice.intrastat_transaction_id)
        invoice.intrastat_transaction_id = self.tr_12
        invoice.intrastat_transport_id = self.transport_rail
        invoice.invoice_incoterm_id = self.incoterm

        move_reversal = (
            self.env["account.move.reversal"]
            .with_context(active_model="account.move", active_ids=invoice.ids)
            .create(
                {
                    "date": fields.Date.from_string("2021-09-02"),
                    "reason": "no reason",
                    "refund_method": "refund",
                    "journal_id": invoice.journal_id.id,
                }
            )
        )
        reversal = move_reversal.reverse_moves()
        in_refund = self.env["account.move"].browse(reversal["res_id"])
        self.assertFalse(in_refund.intrastat_transport_id)
        self.assertFalse(in_refund.invoice_incoterm_id)
        self.assertFalse(in_refund.intrastat_transaction_id)

    def test_in_invoice_reversal(self):
        date_order = "2021-09-01"
        invoice = self._create_in_invoice()
        invoice.invoice_date = fields.Date.from_string(date_order)
        invoice.action_post()
        self.assertFalse(invoice.intrastat_transaction_id)
        invoice.intrastat_transaction_id = self.tr_11
        invoice.intrastat_transport_id = self.transport_rail
        invoice.invoice_incoterm_id = self.incoterm

        move_reversal = (
            self.env["account.move.reversal"]
            .with_context(active_model="account.move", active_ids=invoice.ids)
            .create(
                {
                    "date": fields.Date.from_string("2021-09-02"),
                    "reason": "no reason",
                    "refund_method": "refund",
                    "journal_id": invoice.journal_id.id,
                }
            )
        )
        reversal = move_reversal.reverse_moves()
        in_refund = self.env["account.move"].browse(reversal["res_id"])
        self.assertFalse(in_refund.intrastat_transport_id)
        self.assertFalse(in_refund.invoice_incoterm_id)
        self.assertFalse(in_refund.intrastat_transaction_id)
