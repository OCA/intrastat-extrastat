# -*- coding: utf-8 -*-
# Copyright 2018 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    eori_number = fields.Char(string='EORI Number')
