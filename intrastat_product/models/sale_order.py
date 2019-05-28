# Copyright 2010-2019 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    intrastat_transport_id = fields.Many2one(
        comodel_name='intrastat.transport_mode', string='Transport Mode',
        help="This information is used in Intrastat reports")
    intrastat = fields.Selection(
        string='Intrastat Declaration',
        related='company_id.intrastat_dispatches')

    def _prepare_invoice(self):
        '''Copy destination country to invoice'''
        vals = super(SaleOrder, self)._prepare_invoice()
        if self.intrastat_transport_id:
            vals['intrastat_transport_id'] = self.intrastat_transport_id.id
        if self.warehouse_id.region_id:
            vals['src_dest_region_id'] = self.warehouse_id.region_id.id
        return vals
