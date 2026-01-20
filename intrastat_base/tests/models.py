# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class IntrastatDeclarationTest(models.Model):
    _inherit = ["mail.thread", "mail.activity.mixin", "intrastat.common"]
    _name = "intrastat.declaration.test"
    _description = "Intrastat Declaration Test"
