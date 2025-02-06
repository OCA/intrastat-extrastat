# Copyright 2010-2022 Akretion France (http://www.akretion.com/)
# @author: <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    intrastat_type = fields.Selection(
        [
            ("product", "Product"),
            ("service", "Service"),
        ],
        compute="_compute_intrastat_type",
        store=True,
        precompute=True,
        help="Type of product used for the intrastat declarations.",
    )
    is_accessory_cost = fields.Boolean(
        compute="_compute_is_accessory_cost",
        store=True,
        precompute=True,
        readonly=False,
        help="Activate this option for shipping costs, packaging "
        "costs and all services related to the sale of products. "
        "This option is used for Intrastat reports.",
    )

    @api.depends("type", "combo_ids.combo_item_ids.product_id.type")
    def _compute_intrastat_type(self):
        for this in self:
            intrastat_type = "service"
            if this.type == "consu":
                intrastat_type = "product"
            elif this.type == "combo":
                for combo in this.combo_ids:
                    for item in combo.combo_item_ids:
                        if item.product_id.type == "consu":
                            intrastat_type = "product"
                            break
            this.intrastat_type = intrastat_type

    @api.depends("intrastat_type")
    def _compute_is_accessory_cost(self):
        for this in self:
            if this.intrastat_type != "service":
                this.is_accessory_cost = False

    @api.constrains("intrastat_type", "is_accessory_cost")
    def _check_accessory_cost(self):
        for this in self:
            if this.is_accessory_cost and this.intrastat_type != "service":
                raise ValidationError(
                    _(
                        "The option 'Is accessory cost?' can only be "
                        "activated on 'Service' products. You have activated "
                        "this option for the product '%(product_name)s' which is "
                        "not a service product.",
                        product_name=this.display_name,
                    )
                )
