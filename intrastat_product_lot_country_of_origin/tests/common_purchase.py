# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.intrastat_product.tests.common_purchase import IntrastatPurchaseCommon


class IntrastatPurchaseLotCommon(IntrastatPurchaseCommon):
    def _get_expected_vals(self, line):
        """
        The product of origin should come from lot filled in during
        reception
        """
        res = super()._get_expected_vals(line)
        res.update(
            {
                "product_origin_country_id": self.env.ref("base.it"),
            }
        )
        return res
