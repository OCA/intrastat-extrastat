# Copyright 2020-2021 Akretion France (http://www.akretion.com/)
# @author: <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountFiscalPosition(models.Model):
    _inherit = "account.fiscal.position"

    intrastat = fields.Boolean(
        help="Set to True if the invoices with this fiscal position should "
        "be taken into account for the generation of the intrastat reports.",
    )
