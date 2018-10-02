# -*- coding: utf-8 -*-
# © 2011-2017 Akretion (http://www.akretion.com)
# © 2009-2017 Noviat (http://www.noviat.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# @author Luc de Meyer <info@noviat.com>

from odoo import models, fields, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    # in v10, the sale_stock module defines an incoterms_id
    # Odoo v8 name: incoterm_id
    intrastat_transaction_id = fields.Many2one(
        'intrastat.transaction', string='Intrastat Transaction Type',
        ondelete='restrict', track_visibility='onchange',
        help="Intrastat nature of transaction")
    intrastat_transport_id = fields.Many2one(
        'intrastat.transport_mode', string='Intrastat Transport Mode',
        ondelete='restrict')
    src_dest_country_id = fields.Many2one(
        'res.country', string='Origin/Destination Country',
        compute='_compute_intrastat_country',
        store=True, compute_sudo=True,
        help="Destination country for dispatches. Origin country for "
        "arrivals.")
    intrastat_country = fields.Boolean(
        compute='_compute_intrastat_country', string='Intrastat Country',
        store=True, readonly=True, compute_sudo=True)
    src_dest_region_id = fields.Many2one(
        'intrastat.region', string='Origin/Destination Region',
        default=lambda self: self._default_src_dest_region_id(),
        help="Origin region for dispatches, destination region for "
        "arrivals. This field is used for the Intrastat Declaration.",
        ondelete='restrict')
    intrastat = fields.Char(
        string='Intrastat Declaration',
        related='company_id.intrastat', readonly=True, compute_sudo=True)

    @api.multi
    @api.depends('partner_shipping_id.country_id', 'partner_id.country_id')
    def _compute_intrastat_country(self):
        for inv in self:
            country = inv.partner_shipping_id.country_id\
                or inv.partner_id.country_id
            if not country:
                country = inv.company_id.country_id
            inv.src_dest_country_id = country.id
            inv.intrastat_country = country.intrastat

    @api.model
    def _default_src_dest_region_id(self):
        rco = self.env['res.company']
        company = rco._company_default_get('account.invoice')
        return company.intrastat_region_id


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    hs_code_id = fields.Many2one(
        'hs.code', string='Intrastat Code', ondelete='restrict')

    @api.onchange('product_id')
    def intrastat_product_id_change(self):
        if self.product_id:
            hs_code = self.product_id.get_hs_code_recursively()
            self.hs_code_id = hs_code and hs_code.id or False
