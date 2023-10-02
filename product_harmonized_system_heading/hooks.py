# Copyright 2023 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


def post_init_hook(cr, registry):
    _logger.info("Creating default H.S. Code Headings for H.S. Codes in the System.")
    env = api.Environment(cr, SUPERUSER_ID, {})
    HSCode = env["hs.code"].with_context(active_test=False)
    HSCodeHeading = env["hs.code.heading"].with_context(active_test=False)
    existing_hs_code_heading_codes = HSCodeHeading.search([]).mapped("code")
    to_create_dict = dict()
    hs_code_ids = HSCode.search([])
    for hs_code in hs_code_ids:
        vals = False
        heading_code = hs_code.local_code[:4]
        if heading_code in existing_hs_code_heading_codes:
            continue
        if heading_code not in to_create_dict.keys():
            vals = {"code": heading_code}
            to_create_dict[heading_code] = [hs_code.id]
        else:
            to_create_dict[heading_code].append(hs_code.id)
    vals_list = list()
    for code, rel_hs_code_ids in to_create_dict.items():
        vals = {"code": code, "hs_code_ids": [(6, 0, rel_hs_code_ids)]}
        vals_list.append(vals)
    _logger.info("Creating %s H.S. Code Headings" % len(vals_list))
    HSCodeHeading.create(vals_list)
