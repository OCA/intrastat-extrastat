# -*- coding: utf-8 -*-
# © 2011-2016 Akretion (http://www.akretion.com)
# © 2009-2016 Noviat (http://www.noviat.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# @author Luc de Meyer <info@noviat.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    hs_code_id = fields.Many2one(
        'hs.code', string='H.S. Code',
        company_dependent=True, ondelete='restrict',
        help="Harmonised System Code. Nomenclature is "
        "available from the World Customs Organisation, see "
        "http://www.wcoomd.org/. You can leave this field empty "
        "and configure the H.S. code on the product category.")
    origin_country_id = fields.Many2one(
        'res.country', string='Country of Origin',
        help="Country of origin of the product i.e. product "
        "'made in ____'.")


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.multi
    def get_hs_code_recursively(self):
        res = self.env['hs.code']
        if not self:
            return res
        else:
            self.ensure_one()
            if self.hs_code_id:
                res = self.hs_code_id
            elif self.categ_id:
                res = self.categ_id.get_hs_code_recursively()
            return res
