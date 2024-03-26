# Copyright 2010-2021 Akretion (<alexis.delattre@akretion.com>)
# Copyright 2009-2021 Noviat (http://www.noviat.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class IntrastatResultView(models.TransientModel):
    _name = "intrastat.result.view"
    _description = "Pop-up to show errors on intrastat report generation"

    note = fields.Html(
        string="Notes", readonly=True, default=lambda self: self._context.get("note")
    )
