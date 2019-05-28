# Copyright 2011-2016 Akretion France (http://www.akretion.com)
# Copyright 2009-2016 Noviat (http://www.noviat.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# @author Luc de Meyer <info@noviat.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class HSCode(models.Model):
    _name = "hs.code"
    _description = "H.S. Code"
    _order = "local_code"
    _rec_name = "local_code"

    hs_code = fields.Char(
        string='H.S. Code', compute='_compute_hs_code', readonly=True,
        help="Harmonized System code (6 digits). Full list is "
        "available from the World Customs Organisation, see "
        "http://www.wcoomd.org")
    description = fields.Char(
        translate=True,
        help="Short text description of the H.S. category")
    local_code = fields.Char(
        required=True,
        help="Code used for the national Import/Export declaration. "
        "The national code starts with the 6 digits of the H.S. and often "
        "has a few additional digits to extend the H.S. code.")
    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        'res.company', string='Company', readonly=True, required=True,
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
    product_categ_count = fields.Integer(
        compute='_compute_product_categ_count')
    product_tmpl_count = fields.Integer(compute='_compute_product_tmpl_count')

    @api.depends('local_code')
    def _compute_hs_code(self):
        for this in self:
            this.hs_code = this.local_code and this.local_code[:6]

    @api.depends('product_categ_ids')
    def _compute_product_categ_count(self):
        # hs_code_id on product.category is company_dependent=True
        # so we can't use a read_group()
        for code in self:
            code.product_categ_count = len(code.product_categ_ids)

    @api.depends('product_tmpl_ids')
    def _compute_product_tmpl_count(self):
        # hs_code_id on product.template is company_dependent=True
        # so we can't use a read_group()
        for code in self:
            code.product_tmpl_count = len(code.product_tmpl_ids)

    @api.depends('local_code', 'description')
    def name_get(self):
        res = []
        for this in self:
            name = this.local_code
            if this.description:
                name += ' ' + this.description
            name = len(name) > 55 and name[:55] + '...' or name
            res.append((this.id, name))
        return res

    _sql_constraints = [
        ('local_code_company_uniq', 'unique(local_code, company_id)',
         'This code already exists for this company !'),
    ]

    @api.model
    def create(self, vals):
        if vals.get('local_code'):
            vals['local_code'] = vals['local_code'].replace(' ', '')
        return super(HSCode, self).create(vals)

    def write(self, vals):
        if vals.get('local_code'):
            vals['local_code'] = vals['local_code'].replace(' ', '')
        return super(HSCode, self).write(vals)
