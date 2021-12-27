# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from freezegun import freeze_time

from odoo.tests.common import SavepointCase

from .common_sale import IntrastatSaleCommon


class TestIntrastatProductSale(IntrastatSaleCommon):
    """Tests for this module"""

    def test_sale_to_invoice_default(self):
        self._create_sale_order()
        self.sale.action_confirm()
        self.sale.picking_ids.action_assign()
        for line in self.sale.picking_ids.move_line_ids:
            line.qty_done = line.product_uom_qty
        self.sale.picking_ids._action_done()
        self.assertEqual("done", self.sale.picking_ids.state)

        invoice = self.sale._create_invoices()
        invoice.action_post()

        # Check if transport mode has been transmitted to invoice
        # It should be None as not defined on sale order
        self.assertFalse(
            invoice.intrastat_transport_id,
        )

    # Test specific transport set on sale to invoice
    def test_sale_to_invoice(self):
        self._create_sale_order()
        # Set intrastat transport mode to rail
        self.sale.intrastat_transport_id = self.transport_rail
        self.sale.action_confirm()
        self.sale.picking_ids.action_assign()
        for line in self.sale.picking_ids.move_line_ids:
            line.qty_done = line.product_uom_qty
        self.sale.picking_ids._action_done()
        self.assertEqual("done", self.sale.picking_ids.state)

        invoice = self.sale._create_invoices()
        invoice.action_post()

        # Check if transport mode has been transmitted to invoice
        self.assertEqual(
            self.transport_rail,
            invoice.intrastat_transport_id,
        )

    def test_sale_declaration(self):
        date_order = "2021-09-01"
        declaration_date = "2021-10-01"
        with freeze_time(date_order):
            self._create_sale_order()
        # Set intrastat transport mode to rail
        self.sale.intrastat_transport_id = self.transport_rail
        self.sale.action_confirm()
        self.sale.picking_ids.action_assign()
        for line in self.sale.picking_ids.move_line_ids:
            line.qty_done = line.product_uom_qty
        self.sale.picking_ids._action_done()
        self.assertEqual("done", self.sale.picking_ids.state)

        with freeze_time(date_order):
            invoice = self.sale._create_invoices()
            invoice.action_post()

        # Check if transport mode has been transmitted to invoice
        self.assertEqual(
            self.transport_rail,
            invoice.intrastat_transport_id,
        )
        vals = {
            "declaration_type": "dispatches",
        }
        with freeze_time(declaration_date):
            self._create_declaration(vals)
        self.declaration.action_gather()

        self._check_line_values()
        self.declaration.generate_declaration()
        self._check_line_values(final=True)


class TestIntrastatProductSaleCase(TestIntrastatProductSale, SavepointCase):
    """ Test Intrastat Sale """
