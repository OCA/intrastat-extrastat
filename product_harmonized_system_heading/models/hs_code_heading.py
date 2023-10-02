# Copyright 2023 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class HSCodeHeading(models.Model):
    _name = "hs.code.heading"
    _description = "H.S. Code Heading"

    # General fields
    active = fields.Boolean(default=True)
    code = fields.Char(
        required=True,
        size=4,
        help="The H.S. Code Heading can only have 4 digits, as this define the Heading.",
    )
    description = fields.Text()

    # Relational fields
    hs_code_ids = fields.One2many(
        comodel_name="hs.code",
        inverse_name="hs_code_heading_id",
        string="H.S. Codes",
        readonly=True,
        help="The related H.S. Codes using the Heading.",
    )

    _sql_constraints = [
        (
            "code_uniq",
            "UNIQUE(code)",
            "There is already an existing H.S. Code Heading with this Code.",
        )
    ]

    def _get_name(self):
        self.ensure_one()
        name = self.code
        if self.description:
            name += " " + self.description
        return len(name) > 55 and name[:55] + "..." or name

    def name_get(self):
        res = []
        for rec in self:
            name = rec._get_name()
            res.append((rec.id, name))
        return res
