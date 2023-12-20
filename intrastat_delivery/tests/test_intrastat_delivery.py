# © 2023 FactorLibre - Aritz Olea <aritz.olea@factorlibre.com>
from odoo import Command
from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestIntrastatDelivery(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product_1 = cls.env["product.product"].create(
            {"name": "Service", "type": "consu", "invoice_policy": "order"}
        )
        cls.product_delivery_1 = cls.env["product.product"].create(
            {
                "name": "Delivery Product 1",
                "type": "service",
                "list_price": 10.0,
                "categ_id": cls.env.ref("delivery.product_category_deliveries").id,
            }
        )
        cls.incoterm = cls.env["account.incoterms"].create(
            {"name": "Incoterm", "code": "INC"}
        )
        cls.intrastat_transport_mode = cls.env["intrastat.transport_mode"].create(
            {"name": "Incoterm", "code": "INC", "description": "DESC"}
        )
        cls.carrier = cls.env["delivery.carrier"].create(
            {
                "name": "Test carrier",
                "delivery_type": "fixed",
                "product_id": cls.product_delivery_1.id,
                "incoterm": cls.incoterm.id,
                "intrastat_transport_id": cls.intrastat_transport_mode.id,
            }
        )
        cls.order = cls.env["sale.order"].create(
            {
                "partner_id": cls.partner_a.id,
                "order_line": [
                    Command.create(
                        {
                            "product_id": cls.product_1.id,
                        }
                    ),
                ],
            }
        )
        cls.journal_sale = cls.env["account.journal"].create(
            {
                "name": "Test journal sale",
                "code": "TST-JRNL-S",
                "type": "sale",
                "company_id": cls.env.company.id,
            }
        )

    def test_01_incoterms_intrastat_transport_propagation(self):
        self.assertEqual(self.order.incoterm, self.env["account.incoterms"])
        self.assertEqual(
            self.order.intrastat_transport_id, self.env["intrastat.transport_mode"]
        )
        self.order.set_delivery_line(self.carrier, 0)
        self.assertEqual(self.order.incoterm, self.env["account.incoterms"])
        self.assertEqual(
            self.order.intrastat_transport_id, self.env["intrastat.transport_mode"]
        )
        self.order.action_confirm()
        self.assertEqual(self.order.incoterm, self.incoterm)
        self.assertEqual(
            self.order.intrastat_transport_id, self.intrastat_transport_mode
        )
        self.context = {
            "active_model": "sale.order",
            "active_ids": [self.order.id],
            "active_id": self.order.id,
            "default_journal_id": self.journal_sale.id,
        }
        payment = (
            self.env["sale.advance.payment.inv"]
            .with_context(**self.context)
            .create({"advance_payment_method": "delivered"})
        )
        payment.create_invoices()
        invoice = self.order.invoice_ids[0]
        self.assertEqual(invoice.invoice_incoterm_id, self.incoterm)
        self.assertEqual(invoice.intrastat_transport_id, self.intrastat_transport_mode)
