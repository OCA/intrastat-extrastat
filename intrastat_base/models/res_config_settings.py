# © 2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# © 2018 brain-tec AG (Kumar Aberer <kumar.aberer@braintec-group.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    intrastat_remind_user_ids = fields.Many2many(
        related='company_id.intrastat_remind_user_ids')
