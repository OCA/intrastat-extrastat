# © 2023 FactorLibre - Aritz Olea <aritz.olea@factorlibre.com>
from odoo import fields, models


class DeliveryCarrier(models.Model):
    _inherit = "delivery.carrier"

    incoterm = fields.Many2one(
        comodel_name="account.incoterms",
        help="International Commercial Terms are a series of predefined "
        "commercial terms used in international transactions.",
    )
    intrastat_transport_id = fields.Many2one(
        comodel_name="intrastat.transport_mode",
        string="Intrastat Transport Mode",
    )
