# Copyright 2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# Copyright 2009-2020 Noviat (http://www.noviat.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    intrastat_arrivals = fields.Selection(
        related="company_id.intrastat_arrivals", readonly=False
    )
    intrastat_dispatches = fields.Selection(
        related="company_id.intrastat_dispatches", readonly=False
    )
    intrastat = fields.Char(related="company_id.intrastat")
    intrastat_transport_id = fields.Many2one(
        related="company_id.intrastat_transport_id", readonly=False
    )
    intrastat_region_id = fields.Many2one(
        related="company_id.intrastat_region_id", readonly=False
    )
    intrastat_transaction_out_invoice = fields.Many2one(
        related="company_id.intrastat_transaction_out_invoice", readonly=False
    )
    intrastat_transaction_out_refund = fields.Many2one(
        related="company_id.intrastat_transaction_out_refund", readonly=False
    )
    intrastat_transaction_in_invoice = fields.Many2one(
        related="company_id.intrastat_transaction_in_invoice", readonly=False
    )
    intrastat_transaction_in_refund = fields.Many2one(
        related="company_id.intrastat_transaction_in_refund", readonly=False
    )
    intrastat_accessory_costs = fields.Boolean(
        related="company_id.intrastat_accessory_costs", readonly=False
    )
    country_id = fields.Many2one(related="company_id.country_id")
    country_code = fields.Char(related="company_id.country_id.code")
