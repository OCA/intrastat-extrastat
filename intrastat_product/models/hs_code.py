# Copyright 2011-2020 Akretion (http://www.akretion.com)
# Copyright 2009-2020 Noviat (http://www.noviat.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# @author Luc de Meyer <info@noviat.com>

from odoo import fields, models


class HSCode(models.Model):
    _inherit = "hs.code"

    intrastat_unit_id = fields.Many2one(
        comodel_name="intrastat.unit", string="Intrastat Supplementary Unit"
    )
