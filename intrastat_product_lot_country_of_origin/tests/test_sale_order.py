# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from freezegun import freeze_time

from odoo.tests.common import SavepointCase

from .common_sale import IntrastatSaleLotCommon


class TestIntrastatProductSaleLot(IntrastatSaleLotCommon):
    """Tests for this module"""

    @classmethod
    def _init_lot(cls):
        vals = {
            "name": "Lot from Italy",
            "origin_country_id": cls.env.ref("base.it").id,
            "product_id": cls.product_c3po.product_variant_ids[0].id,
            "company_id": cls.env.company.id,
        }
        cls.product_lot = cls.env["stock.production.lot"].create(vals)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._init_lot()

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
            line.lot_id = self.product_lot
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

    def test_sale_declaration_not_on_lot(self):
        """
        Check if the country is present in the declaration even if
        not on lot but on product
        """
        self.product_lot.origin_country_id = False
        self.product_c3po.origin_country_id = self.env.ref("base.it")
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
            line.lot_id = self.product_lot
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


class TestIntrastatSalePurchaseLotCase(TestIntrastatProductSaleLot, SavepointCase):
    """ Test Intrastat Sale """
