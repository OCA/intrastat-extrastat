# © 2023 FactorLibre - Aritz Olea <aritz.olea@factorlibre.com>
from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _action_confirm(self):
        ret = super()._action_confirm()
        for order in self:
            order.write(
                {
                    "incoterm": order.carrier_id.incoterm.id,
                    "intrastat_transport_id": (
                        order.carrier_id.intrastat_transport_id.id
                    ),
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
