# Copyright 2020 Akretion France (http://www.akretion.com/)
# @author: <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class AccountFiscalPositionTemplate(models.Model):
    _inherit = "account.fiscal.position.template"

    intrastat = fields.Boolean(
        string="Intrastat",
        help="Check this if you want to generate intrastat declarations with"
        "the created fiscal position",
    )
