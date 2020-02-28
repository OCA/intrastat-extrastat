# Copyright 2009-2020 Noviat nv/sa (www.noviat.com).
# @author Luc de Meyer <info@noviat.com>

from odoo import api, fields, models


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

    code = fields.Char(string="Code", required=True)
    country_id = fields.Many2one(
        comodel_name="res.country", string="Country", required=True
    )
    name = fields.Char(string="Name", translate=True)
    description = fields.Char(string="Description")
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda self: self._default_company_id(),
    )

    @api.model
    def _default_company_id(self):
        return self.env.company
