# Copyright 2021 ACSONE SA/NV
# Copyright 2022 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from psycopg2 import IntegrityError

from odoo.exceptions import UserError, ValidationError
from odoo.tests import Form
from odoo.tests.common import TransactionCase
from odoo.tools import mute_logger

from .common import IntrastatProductCommon


class TestIntrastatProduct(IntrastatProductCommon):
    """Tests for this module"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test product",
                "hs_code_id": cls.env.ref("product_harmonized_system.84715000").id,
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

    # Test duplicates
    @mute_logger("odoo.sql_db")
    def test_region(self):
        with self.assertRaises(IntegrityError):
            self._create_region()

    @mute_logger("odoo.sql_db")
    def test_transaction(self):
        self._create_transaction()
        with self.assertRaises(IntegrityError):
            self._create_transaction()

    @mute_logger("odoo.sql_db")
    def test_transport_mode(self):
        vals = {"code": 1, "name": "Sea"}
        with self.assertRaises(IntegrityError):
            self._create_transport_mode(vals)

    def test_copy(self):
        """
        When copying declaration, the new one has an incremented revision
        value.
        """
        vals = {"declaration_type": "dispatches"}
        self._create_declaration(vals)
        decl_copy = self.declaration.copy()
        self.assertEqual(self.declaration.revision + 1, decl_copy.revision)

    def test_declaration_manual_lines(self):
        vals = {"declaration_type": "dispatches"}
        self._create_declaration(vals)
        computation_line_form = Form(
            self.env["intrastat.product.computation.line"].with_context(
                default_parent_id=self.declaration.id
            )
        )
        computation_line_form.src_dest_country_code = "FR"
        computation_line = computation_line_form.save()
        self.assertEqual(computation_line.src_dest_country_code, "FR")
        declaration_line_form = Form(
            self.env["intrastat.product.declaration.line"].with_context(
                default_parent_id=self.declaration.id
            )
        )
        declaration_line_form.src_dest_country_code = "FR"
        declaration_line = declaration_line_form.save()
        self.assertEqual(declaration_line.src_dest_country_code, "FR")

    def test_declaration_no_country(self):
        self.demo_company.country_id = False
        with self.assertRaises(ValidationError):
            self._create_declaration()
            self.declaration.flush()

    def test_declaration_no_vat(self):
        self.demo_company.partner_id.vat = False
        with self.assertRaises(UserError):
            self._create_declaration()
            self.declaration.flush()
            self.declaration._check_generate_xml()

    def test_declaration_state(self):
        self._create_declaration()
        self.declaration.unlink()

        self._create_declaration()
        self.declaration.state = "done"
        with self.assertRaises(UserError):
            self.declaration.unlink()

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
        )._render_qweb_text(self.invoice.ids, False)
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


class TestIntrastatProductCase(TestIntrastatProduct, TransactionCase):
    """Test Intrastat Product"""
