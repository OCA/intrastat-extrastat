# Copyright 2023 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class HSCode(models.Model):
    _inherit = "hs.code"

    hs_code_heading_id = fields.Many2one(
        comodel_name="hs.code.heading", string="H.S. Code Heading", readonly=True
    )

    @api.constrains("local_code")
    def _check_local_code(self):
        for hs_code in self:
            if len(hs_code.local_code) < 4:
                msg = (
                    "The H.S. Local Code needs to have at least 4 characters as this "
                    "indicate the H.S. Heading."
                )
                raise ValidationError(_(msg))

    @api.model
    def _get_hs_code_heading_id(self, vals):
        """
        Method used in the `create` and `write` methods of the `hs.code`.
        Used to get the corresponding H.S. Code Heading based on the `local_code` value
        of the H.S. Code. Get the existing one, if there is, otherwise create a new one.
        :return: a modified vals dict with the `hs_code_heading_id` value
        """
        HSCodeHeading = self.env["hs.code.heading"]
        local_code = vals.get("local_code", "")
        heading_code = local_code[:4]
        heading = HSCodeHeading.search([("code", "=", heading_code)], limit=1)
        if not heading:
            heading = HSCodeHeading.create({"code": heading_code})
        vals["hs_code_heading_id"] = heading.id
        return vals

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals = self._get_hs_code_heading_id(vals)
        return super().create(vals_list)

    def write(self, vals):
        if "local_code" in vals:
            vals = self._get_hs_code_heading_id(vals)
        return super().write(vals)

    def _get_name(self):
        """
        Overwrite method from the `product_harmonized_system` module in order to set the
        Heading Description in the H.S. Code name
        """
        self.ensure_one()
        name = self.local_code
        if self.hs_code_heading_id.description:
            name += " " + self.hs_code_heading_id.description
        if self.description:
            name += ": " + self.description
        return len(name) > 55 and name[:55] + "..." or name
