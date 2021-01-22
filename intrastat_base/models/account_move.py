# Copyright 2020 Akretion France (http://www.akretion.com/)
# @author: <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    intrastat_fiscal_position = fields.Boolean(
        related="fiscal_position_id.intrastat",
        store=True,
        string="Intrastat Fiscal Position",
    )
