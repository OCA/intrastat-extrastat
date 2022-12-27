# Copyright 2010-2022 Akretion France (http://www.akretion.com/)
# @author: <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_accessory_cost = fields.Boolean(
        help="Activate this option for shipping costs, packaging "
        "costs and all services related to the sale of products. "
        "This option is used for Intrastat reports.",
    )

    @api.constrains("type", "is_accessory_cost")
    def _check_accessory_cost(self):
        for this in self:
            if this.is_accessory_cost and this.type != "service":
                raise ValidationError(
                    _(
                        "The option 'Is accessory cost?' should only be "
                        "activated on 'Service' products. You have activated "
                        "this option for the product '{product_name}' which is "
                        "configured with type '{product_type}'."
                    ).format(
                        product_name=this.display_name,
                        product_type=this._fields["type"].convert_to_export(
                            this.type, this
                        ),
                    )
                )
