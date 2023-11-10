# Copyright 2009-2023 Noviat.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import csv
import io
import os

import odoo
from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.osv.expression import OR


class IntrastatHSCodesImportInstaller(models.TransientModel):
    _name = "intrastat.hscodes.import.installer"
    _inherit = "res.config.installer"
    _description = "Intrastat HS Codes Import Installer"

    share_codes = fields.Boolean(
        default=True,
        help="Set this flag to share the Intrastat Codes between all "
        "Legal Entities defined in this Odoo Database.\n",
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
    )

    def _hscodes_vals_domain(self):
        domain = [("company_id", "=", False)]
        if self.company_id:
            domain = OR([domain, ("company_id", "=", self.company_id.id)])
        return domain

    @api.model
    def _load_code(self, row, hs_codes, hscodes_lookup):
        company_id = self.company_id.id or False
        vals = {
            "description": row["description"],
            "company_id": company_id,
        }
        intrastat_unit_id = row["unit_id"]
        if intrastat_unit_id:
            intrastat_unit_ref = "intrastat_product." + intrastat_unit_id
            intrastat_unit = self.env.ref(intrastat_unit_ref)
            vals["intrastat_unit_id"] = intrastat_unit.id
        intrastat_code = row["code"]
        hscode_i = hscodes_lookup.get(intrastat_code)
        if isinstance(hscode_i, int):
            hs_codes[hscode_i].write(vals)
        else:
            vals["local_code"] = intrastat_code
            hscode_rec = self.env["hs.code"].create(vals)
            hs_codes |= hscode_rec
            hscodes_lookup[intrastat_code] = 1
        return hs_codes, hscodes_lookup

    def execute(self):
        res = super().execute()
        # get path for intrastat hs codes files
        module = __name__.split("addons.")[1].split(".")[0]
        module_path = ""
        for adp in odoo.addons.__path__:
            module_path = adp + os.sep + module
            if os.path.isdir(module_path):
                break
        module_path += os.sep + "static/data" + os.sep
        # load existing intrastat codes
        hs_codes = self.env["hs.code"].search(self._hscodes_vals_domain())
        hscodes_lookup = {}
        for i, c in enumerate(hs_codes):
            hscodes_lookup[c.local_code] = i
        # load csv files from data
        lang_found = False
        CN_fns = os.listdir(module_path)
        langs = {x[5:7] for x in CN_fns}
        for lang in langs:
            lang_recs = self.env["res.lang"].search([("code", "=like", lang + "_%")])
            if not lang_recs:
                continue
            lang_found = True
            CN_fn = [x for x in CN_fns if x[5:7] == lang][0]
            with io.open(
                module_path + CN_fn, mode="r", encoding="Windows-1252"
            ) as CN_file:
                intrastat_codes = csv.DictReader(CN_file, delimiter=";")
                for lang_rec in lang_recs:
                    hs_codes = hs_codes.with_context(lang=lang_rec.code)
                    for row in intrastat_codes:
                        hs_codes, hscodes_lookup = self._load_code(
                            row, hs_codes, hscodes_lookup
                        )
        if not lang_found:
            raise UserError(
                _(
                    "None of the languages active on your system are "
                    "available in intrastat codes files [%s]"
                )
                % ",".join(self._intrastat_file_available_langs())
            )
        return res
