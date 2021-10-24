# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests import Form

from .common import IntrastatProductCommon


class IntrastatPurchaseCommon(IntrastatProductCommon):
    """
    We define common flow:
        - Supplier in Germany
    """

    def _get_expected_vals(self, line):
        return {
            "declaration_type": "arrivals",
            "suppl_unit_qty": line.qty_received,
            "hs_code_id": line.product_id.hs_code_id,
            "product_origin_country_id": line.product_id.origin_country_id,
            "amount_company_currency": line.price_subtotal,
            "src_dest_country_id": line.partner_id.country_id,
        }

    def _check_line_values(self, final=False, declaration=None, purchase=None):
        """
        This method allows to test computation lines and declaration
        lines values from original sale order line
        """
        if declaration is None:
            declaration = self.declaration
        if purchase is None:
            purchase = self.purchase
        for line in purchase.order_line:
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
    def _init_supplier(cls, vals=None):
        values = {
            "name": "DE Supplier",
            "country_id": cls.env.ref("base.de").id,
            "property_account_position_id": cls.position.id,
        }
        if vals is not None:
            values.update(vals)
        cls.supplier = cls.partner_obj.create(values)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.purchase_obj = cls.env["purchase.order"]
        cls.move_obj = cls.env["account.move"]
        cls._init_supplier()

    @classmethod
    def _create_purchase_order(cls, vals=None):
        vals = {
            "partner_id": cls.supplier.id,
        }
        purchase_new = cls.purchase_obj.new(vals)
        purchase_new.onchange_partner_id()
        purchase_vals = purchase_new._convert_to_write(purchase_new._cache)
        cls.purchase = cls.purchase_obj.create(purchase_vals)
        with Form(cls.purchase) as purchase_form:
            with purchase_form.order_line.new() as line:
                line.product_id = cls.product_c3po.product_variant_ids[0]
                line.product_qty = 3.0
                # Price should not be void - if no purchase pricelist
                line.price_unit = 150.0
