# -*- coding: utf-8 -*-
# © 2011-2014 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResCountry(models.Model):
    _inherit = 'res.country'

    intrastat = fields.Boolean(
        string='EU Country',
        help="Set to True for all European Union countries.")
