# -*- coding: utf-8 -*-
# © 2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class AccountConfigSettings(models.TransientModel):
    _inherit = 'account.config.settings'

    intrastat_incoterm_id = fields.Many2one(
        related='company_id.intrastat_incoterm_id')
    intrastat_arrivals = fields.Selection(
        related='company_id.intrastat_arrivals')
    intrastat_dispatches = fields.Selection(
        related='company_id.intrastat_dispatches')
    intrastat = fields.Char(related='company_id.intrastat', readonly=True)
    intrastat_transport_id = fields.Many2one(
        related='company_id.intrastat_transport_id')
    intrastat_region_id = fields.Many2one(
        related='company_id.intrastat_region_id')
    intrastat_transaction_out_invoice = fields.Many2one(
        related='company_id.intrastat_transaction_out_invoice')
    intrastat_transaction_out_refund = fields.Many2one(
        related='company_id.intrastat_transaction_out_refund')
    intrastat_transaction_in_invoice = fields.Many2one(
        related='company_id.intrastat_transaction_in_invoice')
    intrastat_transaction_in_refund = fields.Many2one(
        related='company_id.intrastat_transaction_in_refund')
    intrastat_accessory_costs = fields.Boolean(
        related='company_id.intrastat_accessory_costs')
    country_id = fields.Many2one(
        related='company_id.country_id', readonly=True)
