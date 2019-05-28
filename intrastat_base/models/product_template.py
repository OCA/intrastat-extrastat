# Copyright 2010-2016 Akretion (<alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_accessory_cost = fields.Boolean(
        string='Is accessory cost',
        help="Activate this option for shipping costs, packaging "
        "costs and all services related to the sale of products. "
        "This option is used for Intrastat reports.")

    @api.constrains('type', 'is_accessory_cost')
    def _check_accessory_cost(self):
        for this in self:
            if this.is_accessory_cost and this.type != 'service':
                raise ValidationError(
                    _("The option 'Is accessory cost?' should only be "
                        "activated on 'Service' products. You have activated "
                        "this option for the product '%s' which is of type "
                        "'%s'") %
                    (this.name, this.type))
