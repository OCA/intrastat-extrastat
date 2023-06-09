# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests import Form

from .common import IntrastatProductCommon


class IntrastatSaleCommon(IntrastatProductCommon):
    """
    We define common flow:
        - Customer in Netherlands
    """

    def _get_expected_vals(self, line):
        return {
            "declaration_type": "dispatches",
            "suppl_unit_qty": line.qty_delivered,
            "hs_code_id": line.product_id.hs_code_id,
            "product_origin_country_code": line.product_id.origin_country_id.code,
        }

    def _check_line_values(self, final=False, declaration=None, sale=None):
        """
        This method allows to test computation lines and declaration
        lines values from original sale order line
        """
        if declaration is None:
            declaration = self.declaration
        if sale is None:
            sale = self.sale
        for line in sale.order_line:
            expected_vals = self._get_expected_vals(line)
            comp_line = declaration.computation_line_ids.filtered(
                lambda cline: cline.product_id == line.product_id
            )
            self.assertTrue(
                all(comp_line[key] == val for key, val in expected_vals.items())
            )
            if final:
                decl_line = declaration.declaration_line_ids.filtered(
                    lambda dline: comp_line in dline.computation_line_ids
                )
                self.assertTrue(
                    all(decl_line[key] == val for key, val in expected_vals.items())
                )

    @classmethod
    def _init_customer(cls, vals=None):
        values = {
            "name": "Akretion France",
            "country_id": cls.env.ref("base.fr").id,
            "property_account_position_id": cls.position.id,
            "vat": "FR86792377731",
        }
        if vals is not None:
            values.update(vals)
        cls.customer = cls.partner_obj.create(values)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.sale_obj = cls.env["sale.order"]
        cls._init_customer()

    @classmethod
    def _create_sale_order(cls, vals=None):
        vals = {
            "partner_id": cls.customer.id,
        }
        sale_new = cls.sale_obj.new(vals)
        sale_vals = sale_new._convert_to_write(sale_new._cache)
        cls.sale = cls.sale_obj.create(sale_vals)
        with Form(cls.sale) as sale_form:
            with sale_form.order_line.new() as line:
                line.product_id = cls.product_c3po.product_variant_ids[0]
                line.product_uom_qty = 3.0
