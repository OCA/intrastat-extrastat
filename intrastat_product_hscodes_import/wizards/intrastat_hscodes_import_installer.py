# Copyright 2009-2023 Noviat.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import csv
import io
import os

import chardet

import odoo
from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.osv.expression import OR

CHUNK_SIZE = 65536


def get_encoding(filename):
    detector = chardet.UniversalDetector()
    with open(filename, "rb") as fid:
        while not detector.done:
            chunk = fid.read(CHUNK_SIZE)
            detector.feed(chunk)
            if len(chunk) < CHUNK_SIZE:
                break
    detector.close()
    encoding = detector.result.get("encoding", None)
    return encoding


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

    @api.onchange('share_codes')
    def _onchange_share_codes(self):
        for record in self:
            if not record.share_codes and record.company_id:
                record.company_id = False

    def _intrastat_file_available_langs(self, available_lang_recs):
        langs = self.env["res.lang"].search([('active', '=', True)]).mapped('code')
        res = [x for x in langs if x not in available_lang_recs]
        if res:
            return res
        return [_('Not installed any language')]

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
        available_lang_recs = []
        lang_found = False
        # get path for intrastat hs codes files
        module = __name__.split("addons.")[1].split(".")[0]
        module_path = ""
        for adp in odoo.addons.__path__:
            module_path = adp + os.sep + module
            if os.path.isdir(module_path):
                break
        module_path += os.sep + "static/data" + os.sep
        # load existing intrastat codes
        for record in self:
            hs_codes = self.env["hs.code"].search(record._hscodes_vals_domain())
            hscodes_lookup = {}
            for i, c in enumerate(hs_codes):
                hscodes_lookup[c.local_code] = i
            # load csv files from data
            CN_fns = os.listdir(module_path)
            langs = {x[5:7] for x in CN_fns}
            for lang in langs:
                lang_recs = self.env["res.lang"].search([("code", "=like", lang + "_%")])
                available_lang_recs += lang_recs.mapped('code')
                if not lang_recs:
                    continue
                lang_found = True
                CN_fn = [x for x in CN_fns if x[5:7] == lang][0]
                encoding = get_encoding(module_path + CN_fn)
                with io.open(module_path + CN_fn, mode="r", encoding=encoding) as CN_file:
                    intrastat_codes = csv.DictReader(CN_file, delimiter=";")
                    for lang_rec in lang_recs:
                        hs_codes = hs_codes.with_context(lang=lang_rec.code)
                        for row in intrastat_codes:
                            hs_codes, hscodes_lookup = record._load_code(row, hs_codes, hscodes_lookup)
        if not lang_found:
            raise UserError(
                _(
                    "None of the languages active on your system are "
                    "available in intrastat codes files [%s]"
                )
                % ",".join(self._intrastat_file_available_langs(available_lang_recs))
            )
        return res
