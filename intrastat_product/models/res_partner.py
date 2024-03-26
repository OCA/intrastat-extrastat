# Copyright 2022 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResParter(models.Model):
    _inherit = "res.partner"

    invoice_intrastat_detail = fields.Boolean(
        string="Show intrastat details in invoice report"
    )

    @api.model
    def _commercial_fields(self):
        return super()._commercial_fields() + ["invoice_intrastat_detail"]
