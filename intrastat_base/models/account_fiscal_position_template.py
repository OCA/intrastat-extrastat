# Copyright 2020-2022 Akretion France (http://www.akretion.com/)
# @author: <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class AccountFiscalPositionTemplate(models.Model):
    _inherit = "account.fiscal.position.template"

    intrastat = fields.Selection(
        "_intrastat_selection",
        help="When set to B2B or B2C, the invoices with this fiscal position will "
        "be taken into account for the generation of the intrastat reports.",
    )

    @api.model
    def _intrastat_selection(self):
        return self.env["account.fiscal.position"]._intrastat_selection()
