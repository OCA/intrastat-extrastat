# © 2023 FactorLibre - Aritz Olea <aritz.olea@factorlibre.com>
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    incoterm = fields.Many2one(
        "account.incoterms",
        compute="_compute_incoterm",
        store=True,
        readonly=False,
    )

    def _get_sale_type_incoterm(self):
        """Check if type_id (sale_order_type module) exists and
        consider its incoterm  if is defined."""
        self.ensure_one()
        if "type_id" in self._fields and self.type_id:
            return getattr(self.type_id, "incoterm_id", False)
        return False

    def _get_default_incoterm(self):
        self.ensure_one()
        sale_type_inc = self._get_sale_type_incoterm()
        return (
            sale_type_inc
            or self.partner_id.sale_incoterm_id
            or self.carrier_id.incoterm
            or self.company_id.incoterm_id
            or self.env["account.incoterms"]
        )

    @api.depends(
        "partner_id",
        "partner_id.sale_incoterm_id",
        "carrier_id",
        "carrier_id.incoterm",
        "company_id",
        "company_id.incoterm_id",
    )
    def _compute_incoterm(self):
        for order in self:
            order.incoterm = order._get_default_incoterm()

    def _action_confirm(self):
        ret = super()._action_confirm()
        for order in self:
            incoterm = order._get_default_incoterm()
            intr_trans = (
                order.carrier_id.intrastat_transport_id if order.carrier_id else False
            )
            order.write(
                {
                    "incoterm": incoterm.id,
                    "intrastat_transport_id": intr_trans.id if intr_trans else False,
                }
            )
        return ret

    def _prepare_invoice(self):
        ret = super()._prepare_invoice()
        ret.update(
            {
                "invoice_incoterm_id": self.incoterm.id,
                "intrastat_transport_id": self.intrastat_transport_id.id,
            }
        )
        return ret
