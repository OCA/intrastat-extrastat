# Copyright 2020-2022 Akretion France (http://www.akretion.com/)
# @author: <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class AccountFiscalPosition(models.Model):
    _inherit = "account.fiscal.position"

    intrastat = fields.Selection(
        "_intrastat_selection",
        help="When set to B2B or B2C, the invoices with this fiscal position will "
        "be taken into account for the generation of the intrastat reports.",
    )
    vat_required = fields.Boolean(
        compute="_compute_vat_required", store=True, readonly=False, precompute=True
    )

    @api.model
    def _intrastat_selection(self):
        return [
            ("b2b", self.env._("B2B")),
            ("b2c", self.env._("B2C")),
            ("no", self.env._("No")),
        ]

    @api.constrains("intrastat", "vat_required")
    def _check_intrastat(self):
        for position in self:
            if position.intrastat == "b2b" and not position.vat_required:
                raise ValidationError(
                    self.env._(
                        "The fiscal position '%s' has intrastat set to B2B, "
                        "so the option 'VAT Required' must be enabled.",
                        position.display_name,
                    )
                )
            elif position.intrastat == "b2c" and position.vat_required:
                raise ValidationError(
                    self.env._(
                        "The fiscal position '%s' has intrastat set to B2C, "
                        "so the option 'VAT Required' mustn't be enabled.",
                        position.display_name,
                    )
                )

    @api.depends("intrastat")
    def _compute_vat_required(self):
        for fp in self:
            if fp.intrastat == "b2b" and not fp.vat_required:
                fp.vat_required = True
            elif fp.intrastat == "b2c" and fp.vat_required:
                fp.vat_required = False
