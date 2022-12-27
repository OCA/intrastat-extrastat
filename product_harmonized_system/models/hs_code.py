# Copyright 2011-2022 Akretion France (http://www.akretion.com)
# Copyright 2009-2022 Noviat (http://www.noviat.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# @author Luc de Meyer <info@noviat.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from textwrap import shorten

from odoo import api, fields, models


class HSCode(models.Model):
    _name = "hs.code"
    _description = "H.S. Code"
    _order = "local_code"
    _rec_name = "local_code"

    hs_code = fields.Char(
        string="H.S. Code",
        compute="_compute_hs_code",
        store=True,
        precompute=True,
        help="Harmonized System code (6 digits). Full list is "
        "available from the World Customs Organisation, see "
        "http://www.wcoomd.org",
    )
    description = fields.Char(
        translate=True, help="Short text description of the H.S. category"
    )
    local_code = fields.Char(
        required=True,
        help="Code used for the national Import/Export declaration. "
        "The national code starts with the 6 digits of the H.S. and often "
        "has a few additional digits to extend the H.S. code.",
    )
    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        default=lambda self: self._default_company_id(),
    )
    product_categ_ids = fields.One2many(
        comodel_name="product.category",
        inverse_name="hs_code_id",
        string="Product Categories",
        readonly=True,
    )
    product_tmpl_ids = fields.One2many(
        comodel_name="product.template",
        inverse_name="hs_code_id",
        string="Products",
        readonly=True,
    )
    product_categ_count = fields.Integer(compute="_compute_product_categ_count")
    product_tmpl_count = fields.Integer(compute="_compute_product_tmpl_count")

    @api.model
    def _default_company_id(self):
        return False

    @api.depends("local_code")
    def _compute_hs_code(self):
        for this in self:
            this.hs_code = this.local_code and this.local_code[:6]

    @api.depends("product_categ_ids")
    def _compute_product_categ_count(self):
        rg_res = self.env["product.category"].read_group(
            [("hs_code_id", "in", self.ids)], ["hs_code_id"], ["hs_code_id"]
        )
        mapped_data = {x["hs_code_id"][0]: x["hs_code_id_count"] for x in rg_res}
        for code in self:
            code.product_categ_count = mapped_data.get(code.id, 0)

    @api.depends("product_tmpl_ids")
    def _compute_product_tmpl_count(self):
        rg_res = self.env["product.template"].read_group(
            [("hs_code_id", "in", self.ids)], ["hs_code_id"], ["hs_code_id"]
        )
        mapped_data = {x["hs_code_id"][0]: x["hs_code_id_count"] for x in rg_res}
        for code in self:
            code.product_tmpl_count = mapped_data.get(code.id, 0)

    @api.depends("local_code", "description")
    def name_get(self):
        res = []
        for this in self:
            name = this.local_code
            if this.description:
                name += " " + this.description
            name = shorten(name, 55)
            res.append((this.id, name))
        return res

    _sql_constraints = [
        (
            "local_code_company_uniq",
            "unique(local_code, company_id)",
            "This code already exists for this company !",
        )
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("local_code"):
                vals["local_code"] = vals["local_code"].replace(" ", "")
        return super().create(vals_list)

    def write(self, vals):
        if vals.get("local_code"):
            vals["local_code"] = vals["local_code"].replace(" ", "")
        return super().write(vals)
