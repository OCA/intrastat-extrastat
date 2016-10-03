# -*- coding: utf-8 -*-
# © 2011-2017 Akretion (http://www.akretion.com)
# © 2009-2017 Noviat (http://www.noviat.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# @author Luc de Meyer <info@noviat.com>

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HSCode(models.Model):
    _inherit = "hs.code"

    intrastat_unit_id = fields.Many2one(
        'intrastat.unit', string='Intrastat Supplementary Unit')

    @api.constrains('local_code')
    def _hs_code(self):
        if self.company_id.country_id.intrastat:
            if not self.local_code.isdigit():
                raise ValidationError(_(
                    "Intrastat Codes should only contain digits. "
                    "This is not the case for code '%s'.")
                    % self.local_code)
            if len(self.local_code) != 8:
                raise ValidationError(_(
                    "Intrastat Codes should "
                    "contain 8 digits. This is not the case for "
                    "Intrastat Code '%s' which has %d digits.")
                    % (self.local_code, len(self.local_code)))
