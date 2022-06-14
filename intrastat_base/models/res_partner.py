# Copyright 2022 Noviat.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, models
from odoo.exceptions import UserError

XI_COUNTY_NAMES = [
    "antrim",
    "armagh",
    "down",
    "fermanagh",
    "londonderry",
    "tyrone",
    "northern ireland",
]

XI_COUNTIES = [
    "base.state_uk18",  # County Antrim
    "base.state_uk19",  # County Armagh
    "base.state_uk20",  # County Down
    "base.state_uk22",  # County Fermanagh
    "base.state_uk23",  # County Londonderry
    "base.state_uk24",  # County Tyrone
    "base.state_ie_27",  # Antrim
    "base.state_ie_28",  # Armagh
    "base.state_ie_29",  # Down
    "base.state_ie_30",  # Fermanagh
    "base.state_ie_31",  # Londonderry
    "base.state_ie_32",  # Tyrone
]


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def _get_xi_counties(self):
        return [self.env.ref(x) for x in XI_COUNTIES]

    @api.model
    def _get_xu_counties(self):
        uk_counties = self.env.ref("base.uk").state_ids
        xu_counties = uk_counties.filtered(lambda r: r not in self._get_xi_counties())
        return xu_counties

    def _get_intrastat_country_code(self, country=None, state=None):
        if self:
            self.ensure_one()
            country = self.country_id
            state = self.state_id
        else:
            state = state or self.env["res.country.state"]
            country = country or state.country_id
            if not country:
                raise UserError(
                    _("Programming Error when calling '_get_intrastat_country_code()")
                )
        cc = country.code
        if cc == "GB":
            cc = "XU"
        if state and cc in ["XU", "IE"]:
            if (
                state in self._get_xi_counties()
                or state.name.lower().strip() in XI_COUNTY_NAMES
            ):
                cc = "XI"
        return cc
