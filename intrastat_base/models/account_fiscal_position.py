# Copyright 2020-2022 Akretion France (http://www.akretion.com/)
# @author: <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AccountFiscalPosition(models.Model):
    _inherit = "account.fiscal.position"

    intrastat = fields.Selection(
        "_intrastat_selection",
        help="When set to B2B or B2C, the invoices with this fiscal position will "
        "be taken into account for the generation of the intrastat reports.",
    )

    @api.model
    def _intrastat_selection(self):
        return [
            ("b2b", _("B2B")),
            ("b2c", _("B2C")),
            ("no", _("No")),
        ]

    @api.constrains("intrastat", "vat_required")
    def _check_intrastat(self):
        for position in self:
            if position.intrastat == "b2b" and not position.vat_required:
                raise ValidationError(
                    _(
                        "The fiscal position '%s' has intrastat set to B2B, "
                        "so the option 'VAT Required' must be enabled."
                    )
                    % position.display_name
                )
            elif position.intrastat == "b2c" and position.vat_required:
                raise ValidationError(
                    _(
                        "The fiscal position '%s' has intrastat set to B2C, "
                        "so the option 'VAT Required' mustn't be enabled."
                    )
                    % position.display_name
                )

    @api.onchange("intrastat", "vat_required")
    def intrastat_change(self):
        if self.intrastat == "b2b" and not self.vat_required:
            self.vat_required = True
        elif self.intrastat == "b2c" and self.vat_required:
            self.vat_required = False
