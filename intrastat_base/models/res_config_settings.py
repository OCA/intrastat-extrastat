# Copyright 2017-2020 Akretion France (http://www.akretion.com/)
# Copyright 2018-2020 brain-tec AG (Kumar Aberer <kumar.aberer@braintec-group.com>)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    intrastat_remind_user_ids = fields.Many2many(
        related="company_id.intrastat_remind_user_ids", readonly=False
    )
