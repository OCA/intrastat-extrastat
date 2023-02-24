# Copyright 2022 Noviat.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import Form, TransactionCase

from .common import IntrastatProductCommon


class TestIntrastatBrexit(IntrastatProductCommon, TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.inv_obj = cls.env["account.move"]
        cls.hs_code_whiskey = cls.env["hs.code"].create(
            {
                "description": "Whiskey",
                "local_code": "22083000",
            }
        )
        cls.product_xi = cls.env["product.product"].create(
            {
                "name": "Bushmills Original",
                "weight": 1.4,
                "list_price": 30.0,
                "standard_price": 15.0,
                "origin_country_id": cls.env.ref("base.uk").id,
                "origin_state_id": cls.env.ref("base.state_uk18").id,
                "hs_code_id": cls.hs_code_whiskey.id,
            }
        )
        cls.product_xu = cls.env["product.product"].create(
            {
                "name": "Glenfiddich",
                "weight": 1.4,
                "list_price": 50.0,
                "standard_price": 25.0,
                "origin_country_id": cls.env.ref("base.uk").id,
                "origin_state_id": cls.env.ref("base.state_uk6").id,
                "hs_code_id": cls.hs_code_whiskey.id,
            }
        )
        cls.partner_xi = cls.env["res.partner"].create(
            {
                "name": "Bushmills Distillery",
                "country_id": cls.env.ref("base.uk").id,
                "state_id": cls.env.ref("base.state_uk18").id,
                "vat": "XI123456782",
                "property_account_position_id": cls.position.id,
            }
        )

    def test_brexit_sale(self):
        inv_out_xi = self.inv_obj.with_context(default_move_type="out_invoice").create(
            {
                "partner_id": self.partner_xi.id,
                "partner_shipping_id": self.partner_xi.id,
                "fiscal_position_id": self.position.id,
            }
        )
        with Form(inv_out_xi) as inv_form:
            with inv_form.invoice_line_ids.new() as ail:
                ail.product_id = self.product_c3po.product_variant_ids[0]
        inv_out_xi.action_post()

        self._create_declaration(
            {
                "declaration_type": "dispatches",
                "year": str(inv_out_xi.date.year),
                "month": str(inv_out_xi.date.month).zfill(2),
            }
        )
        self.declaration.action_gather()
        self.declaration.generate_declaration()
        cline = self.declaration.computation_line_ids
        dline = self.declaration.declaration_line_ids
        self.assertEqual(cline.src_dest_country_code, "XI")
        self.assertEqual(dline.src_dest_country_code, "XI")

    def test_brexit_purchase(self):
        inv_in_xi = self.inv_obj.with_context(default_move_type="in_invoice").create(
            {
                "partner_id": self.partner_xi.id,
                "fiscal_position_id": self.position.id,
            }
        )
        with Form(inv_in_xi) as inv_form:
            with inv_form.invoice_line_ids.new() as ail:
                ail.product_id = self.product_xi
            with inv_form.invoice_line_ids.new() as ail:
                ail.product_id = self.product_xu
        inv_in_xi.invoice_date = inv_in_xi.date
        inv_in_xi.action_post()

        self._create_declaration(
            {
                "declaration_type": "arrivals",
                "year": str(inv_in_xi.date.year),
                "month": str(inv_in_xi.date.month).zfill(2),
            }
        )
        self.declaration.action_gather()
        self.declaration.generate_declaration()
        clines = self.declaration.computation_line_ids
        cl_xi = clines.filtered(lambda r: r.product_id == self.product_xi)
        cl_xu = clines.filtered(lambda r: r.product_id == self.product_xu)
        dlines = self.declaration.declaration_line_ids
        dl_xi = dlines.filtered(lambda r: r.computation_line_ids == cl_xi)
        dl_xu = dlines.filtered(lambda r: r.computation_line_ids == cl_xu)
        self.assertEqual(cl_xi.product_origin_country_code, "XI")
        self.assertEqual(cl_xu.product_origin_country_code, "XU")
        self.assertEqual(dl_xi.product_origin_country_code, "XI")
        self.assertEqual(dl_xu.product_origin_country_code, "XU")

    def test_brexit_invoice_intrastat_details(self):
        inv_in_xi = self.inv_obj.with_context(default_move_type="in_invoice").create(
            {
                "partner_id": self.partner_xi.id,
                "fiscal_position_id": self.position.id,
            }
        )
        with Form(inv_in_xi) as inv_form:
            with inv_form.invoice_line_ids.new() as ail:
                ail.product_id = self.product_xi
        inv_in_xi.invoice_date = inv_in_xi.date
        inv_in_xi.compute_intrastat_lines()
        ilines = inv_in_xi.intrastat_line_ids
        self.assertEqual(ilines.product_origin_country_code, "XI")
