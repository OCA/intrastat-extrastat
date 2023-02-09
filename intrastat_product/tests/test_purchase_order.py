# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from freezegun import freeze_time

from odoo import fields
from odoo.tests.common import TransactionCase

from .common_purchase import IntrastatPurchaseCommon


class TestIntrastatProductPurchase(IntrastatPurchaseCommon):
    """Tests for this module"""

    def test_purchase_to_invoice_default(self):
        date_order = "2021-09-01"
        declaration_date = "2021-10-01"
        with freeze_time(date_order):
            self._create_purchase_order()
        self.purchase.button_confirm()
        self.purchase.picking_ids.action_assign()
        for line in self.purchase.picking_ids.move_line_ids:
            line.qty_done = line.reserved_uom_qty
        self.purchase.picking_ids._action_done()
        self.assertEqual("done", self.purchase.picking_ids.state)

        with freeze_time(date_order):
            action = self.purchase.action_create_invoice()
        invoice_id = action["res_id"]
        invoice = self.move_obj.browse(invoice_id)

        invoice.invoice_date = fields.Date.from_string(date_order)
        invoice.action_post()

        # Check if transport mode has been transmitted to invoice
        # It should be None as not defined on sale order
        self.assertFalse(
            invoice.intrastat_transport_id,
        )

        vals = {
            "declaration_type": "arrivals",
        }
        with freeze_time(declaration_date):
            self._create_declaration(vals)
        self.declaration.action_gather()

        self._check_line_values()
        self.declaration.done()
        self._check_line_values(final=True)

        # Check the Excel file
        file_data = self._create_xls()
        self.check_xls(file_data[0])


class TestIntrastatProductPurchaseCase(TestIntrastatProductPurchase, TransactionCase):
    """Test Intrastat Purchase"""
