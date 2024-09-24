#   Copyright (c) 2024 Groupe Voltaire
#   @author Emilie SOUTIRAS  <emilie.soutiras@groupevoltaire.com>
#   License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging

from odoo import models

_logger = logging.getLogger(__name__)


class ProductCategory(models.Model):
    _inherit = "product.category"

    def get_hs_code_recursively(self):
        self.ensure_one()
        if self.hs_code_id:
            res = self.hs_code_id.filter_per_country()
        else:
            res = super().get_hs_code_recursively()
        return res
