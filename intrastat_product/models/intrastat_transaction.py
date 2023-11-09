# Copyright 2011-2020 Akretion France (http://www.akretion.com)
# Copyright 2009-2020 Noviat (http://www.noviat.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# @author Luc de Meyer <info@noviat.com>

from textwrap import shorten

from odoo import api, fields, models


class IntrastatTransaction(models.Model):
    _name = "intrastat.transaction"
    _description = "Intrastat Transaction"
    _rec_name = "code"
    _order = "code"
    _sql_constraints = [
        (
            "intrastat_transaction_code_unique",
            "UNIQUE(code, company_id)",
            "Code must be unique.",
        )
    ]

    code = fields.Char(required=True)
    description = fields.Text(translate=True)
    # intrastat.transaction are shared among companies by default
    company_id = fields.Many2one("res.company")
    active = fields.Boolean(default=True)

    @api.depends("code", "description")
    def name_get(self):
        res = []
        for this in self:
            name = this.code
            if this.description:
                name += " " + this.description
            name = shorten(name, 55)
            res.append((this.id, name))
        return res
