# Copyright 2009-2020 Noviat nv/sa (www.noviat.com).
# @author Luc de Meyer <info@noviat.com>

from odoo import fields, models


class IntrastatRegion(models.Model):
    _name = "intrastat.region"
    _description = "Intrastat Region"
    _sql_constraints = [
        (
            "intrastat_region_code_unique",
            "UNIQUE(code, country_id)",  # TODO add company_id ?
            "Code must be unique.",
        )
    ]

    code = fields.Char(required=True)
    country_id = fields.Many2one(comodel_name="res.country", required=True)
    name = fields.Char(translate=True)
    description = fields.Char()
    company_id = fields.Many2one("res.company")
