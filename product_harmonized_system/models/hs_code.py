# -*- coding: utf-8 -*-
# © 2011-2016 Akretion (http://www.akretion.com)
# © 2009-2018 Noviat (http://www.noviat.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# @author Luc de Meyer <info@noviat.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class HSCode(models.Model):
    _name = "hs.code"
    _description = "H.S. Code"
    _order = "local_code"
    _rec_name = "display_name"

    hs_code = fields.Char(
        string='H.S. Code', compute='_compute_hs_code', readonly=True,
        help="Harmonized System code (6 digits). Full list is "
        "available from the World Customs Organisation, see "
        "http://www.wcoomd.org")
    description = fields.Char(
        'Description', translate=True,
        help="Short text description of the H.S. category")
    display_name = fields.Char(
        compute='_compute_display_name_field', string="Display Name",
        store=True, readonly=True)
    local_code = fields.Char(
        string='Local Code', required=True,
        help="Code used for the national Import/Export declaration. "
        "The national code starts with the 6 digits of the H.S. and often "
        "has a few additional digits to extend the H.S. code.")
    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env['res.company']._company_default_get())
    product_categ_ids = fields.One2many(
        comodel_name='product.category',
        inverse_name='hs_code_id',
        string='Product Categories',
        readonly=True)
    product_tmpl_ids = fields.One2many(
        comodel_name='product.template',
        inverse_name='hs_code_id',
        string='Products',
        readonly=True)

    @api.multi
    @api.depends('local_code')
    def _compute_hs_code(self):
        for this in self:
            this.hs_code = this.local_code and this.local_code[:6]

    @api.multi
    @api.depends('local_code', 'description')
    def _compute_display_name_field(self):
        for this in self:
            display_name = this.local_code
            if this.description:
                display_name += ' ' + this.description
            this.display_name = len(display_name) > 55 \
                and display_name[:55] + '...' \
                or display_name

    _sql_constraints = [
        ('local_code_company_uniq', 'unique(local_code, company_id)',
         'This code already exists for this company !'),
        ]

    @api.model
    def create(self, vals):
        if vals.get('local_code'):
            vals['local_code'] = vals['local_code'].replace(' ', '')
        return super(HSCode, self).create(vals)

    @api.multi
    def write(self, vals):
        if vals.get('local_code'):
            vals['local_code'] = vals['local_code'].replace(' ', '')
        return super(HSCode, self).write(vals)
