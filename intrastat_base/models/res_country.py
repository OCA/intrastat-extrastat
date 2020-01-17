# Copyright 2011-2019 Akretion France (http://www.akretion.com/)
# @author: <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCountry(models.Model):
    _inherit = "res.country"

    intrastat = fields.Boolean(
        string="EU Country", help="Set to True for all European Union countries."
    )
