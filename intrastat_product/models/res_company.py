# -*- coding: utf-8 -*-
# © 2011-2017 Akretion (http://www.akretion.com)
# © 2009-2017 Noviat (http://www.noviat.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# @author Luc de Meyer <info@noviat.com>

from odoo import models, fields, api


class ResCompany(models.Model):
    _inherit = 'res.company'

    intrastat_incoterm_id = fields.Many2one(
        'stock.incoterms',
        string='Default Incoterm for Intrastat',
        help="International Commercial Terms are a series of "
             "predefined commercial terms used in international "
             "transactions.")
    intrastat_arrivals = fields.Selection(
        '_intrastat_arrivals', string='Arrivals',
        default='extended', required=True)
    intrastat_dispatches = fields.Selection(
        '_intrastat_dispatches', string='Dispatches',
        default='extended', required=True)
    intrastat_transport_id = fields.Many2one(
        'intrastat.transport_mode',
        string='Default Transport Mode', ondelete='restrict')
    intrastat = fields.Char(
        string='Intrastat Declaration', store=True, readonly=True,
        compute='_compute_intrastat')
    intrastat_region_id = fields.Many2one(
        'intrastat.region',
        string='Default Intrastat Region')
    intrastat_transaction_out_invoice = fields.Many2one(
        'intrastat.transaction',
        string='Default Intrastat Transaction For Customer Invoice')
    intrastat_transaction_out_refund = fields.Many2one(
        'intrastat.transaction',
        string='Default Intrastat Transaction for Customer Refunds')
    intrastat_transaction_in_invoice = fields.Many2one(
        'intrastat.transaction',
        string='Default Intrastat Transaction For Supplier Invoices')
    intrastat_transaction_in_refund = fields.Many2one(
        'intrastat.transaction',
        string='Default Intrastat Transaction For Supplier Refunds')
    intrastat_accessory_costs = fields.Boolean(
        string='Include Accessory Costs in Fiscal Value of Product')

    @api.model
    def _intrastat_arrivals(self):
        return [
            ('exempt', 'Exempt'),
            ('standard', 'Standard'),
            ('extended', 'Extended')]

    @api.model
    def _intrastat_dispatches(self):
        return [
            ('exempt', 'Exempt'),
            ('standard', 'Standard'),
            ('extended', 'Extended')]

    @api.multi
    @api.depends('intrastat_arrivals', 'intrastat_dispatches')
    def _compute_intrastat(self):
        for this in self:
            if this.intrastat_arrivals == 'exempt' \
                    and this.intrastat_dispatches == 'exempt':
                this.intrastat = 'exempt'
            elif this.intrastat_arrivals == 'extended' \
                    or this.intrastat_dispatches == 'extended':
                this.intrastat = 'extended'
            else:
                this.intrastat = 'standard'
