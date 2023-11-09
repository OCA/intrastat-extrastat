# Copyright 2011-2020 Akretion France (http://www.akretion.com)
# Copyright 2009-2022 Noviat (http://www.noviat.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# @author Luc de Meyer <info@noviat.com>

from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    intrastat_transaction_id = fields.Many2one(
        comodel_name="intrastat.transaction",
        string="Intrastat Transaction Type",
        ondelete="restrict",
        tracking=True,
        check_company=True,
        help="Intrastat Nature of Transaction",
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
    )
    intrastat_transport_id = fields.Many2one(
        comodel_name="intrastat.transport_mode",
        string="Intrastat Transport Mode",
        ondelete="restrict",
    )
    src_dest_country_id = fields.Many2one(
        comodel_name="res.country",
        string="Origin/Destination Country",
        compute="_compute_src_dest_country_id",
        store=True,
        help="Destination country for dispatches. Origin country for arrivals.",
    )
    src_dest_region_id = fields.Many2one(
        comodel_name="intrastat.region",
        string="Origin/Destination Region",
        default=lambda self: self.env.company.intrastat_region_id,
        help="Origin region for dispatches, destination region for "
        "arrivals. This field is used for the Intrastat Declaration.",
        ondelete="restrict",
    )
    intrastat = fields.Char(
        string="Intrastat Declaration", related="company_id.intrastat"
    )
    intrastat_line_ids = fields.One2many(
        comodel_name="account.move.intrastat.line",
        inverse_name="move_id",
        string="Intrastat Declaration Details",
    )

    @api.depends("partner_shipping_id.country_id", "partner_id.country_id")
    def _compute_src_dest_country_id(self):
        for inv in self:
            country = inv.partner_shipping_id.country_id or inv.partner_id.country_id
            if not country:
                country = inv.company_id.country_id
            inv.src_dest_country_id = country.id

    def compute_intrastat_lines(self):
        """
        Compute the Intrastat Lines so that they can be modified
        when encoding the Customer/Supplier Invoice.
        """
        self.mapped("intrastat_line_ids").unlink()
        for inv in self:
            if inv.move_type not in (
                "out_invoice",
                "out_refund",
                "in_invoice",
                "in_refund",
            ):
                continue
            line_vals = []
            for line in inv.invoice_line_ids:
                vals = self._get_intrastat_line_vals(line)
                if vals:
                    line_vals.append(vals)
            if line_vals:
                inv.intrastat_line_ids = [(0, 0, x) for x in line_vals]

    def _get_intrastat_line_vals(self, line):
        vals = {}
        decl_model = self.env["intrastat.product.declaration"]
        notedict, key2label = decl_model._prepare_notedict()
        if decl_model._is_product(line):
            hs_code = line.product_id.get_hs_code_recursively()
            if not hs_code:
                return vals
            weight, qty = decl_model._get_weight_and_supplunits(line, hs_code, notedict)
            vals.update(
                {
                    "invoice_line_id": line.id,
                    "hs_code_id": hs_code.id,
                    "transaction_weight": weight,
                    "transaction_suppl_unit_qty": qty,
                    "product_origin_country_id": line.product_id.origin_country_id.id,
                }
            )
        return vals

    def _prepare_intrastat_line_info(self, line):
        is_intrastat_line = bool(line._name == "account.move.intrastat.line")
        product = line.product_id
        return {
            "product_id": product,
            "hs_code_id": (
                line.hs_code_id if is_intrastat_line else product.hs_code_id
            ),
            "weight": (
                line.transaction_weight
                if is_intrastat_line
                else self._get_intrastat_line_vals(line)["transaction_weight"]
            ),
            "origin_country_id": (
                line.product_origin_country_id
                if is_intrastat_line
                else product.origin_country_id
            ),
        }

    def _get_intrastat_lines_info(self):
        """We obtain a list of information that we will need to group at the end by
        product and sum weight.
        """
        res = {}
        for line in (
            self.invoice_line_ids.filtered(
                lambda x: x.product_id.hs_code_id and x.product_id.origin_country_id
            )
            if not self.intrastat_line_ids
            else self.intrastat_line_ids
        ):
            res.setdefault(line.product_id.id, {"weight": 0})
            vals = self._prepare_intrastat_line_info(line)
            weight = vals.pop("weight")
            res[line.product_id.id].update(vals)
            res[line.product_id.id]["weight"] += weight
        return res.values()


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    hs_code_id = fields.Many2one(
        comodel_name="hs.code",
        compute="_compute_hs_code_id",
        string="Intrastat Code",
    )

    def _compute_hs_code_id(self):
        for rec in self:
            intrastat_line = self.move_id.intrastat_line_ids.filtered(
                lambda r: r.invoice_line_id == rec
            )
            rec.hs_code_id = (
                intrastat_line.hs_code_id or rec.product_id.get_hs_code_recursively()
            )


class AccountMoveIntrastatLine(models.Model):
    _name = "account.move.intrastat.line"
    _description = "Intrastat declaration details"
    _order = "sequence"

    move_id = fields.Many2one(
        comodel_name="account.move",
        string="Invoice",
        ondelete="cascade",
        required=True,
    )
    invoice_line_id = fields.Many2one(
        comodel_name="account.move.line",
        string="Invoice Line",
        ondelete="cascade",
        required=True,
    )
    sequence = fields.Integer(related="invoice_line_id.sequence", store=True)
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
        related="invoice_line_id.product_id",
    )
    quantity = fields.Float(related="invoice_line_id.quantity")
    transaction_suppl_unit_qty = fields.Float(
        help="Transaction quantity in Intrastat Supplementary Unit"
    )
    hs_code_id = fields.Many2one(
        comodel_name="hs.code",
        string="Intrastat Code",
        ondelete="restrict",
        required=True,
    )
    transaction_weight = fields.Integer(
        help="Transaction weight in Kg: Quantity x Product Weight"
    )
    product_origin_country_id = fields.Many2one(
        comodel_name="res.country",
        string="Country of Origin of the Product",
        help="Country of origin of the product i.e. product " "'made in ____'.",
    )

    @api.onchange("invoice_line_id")
    def _onchange_move_id(self):
        moves = self.mapped("move_id")
        dom = [
            ("display_type", "=", "product"),
            ("id", "in", moves.mapped("invoice_line_ids").ids),
            ("id", "not in", moves.mapped("intrastat_line_ids.invoice_line_id").ids),
        ]
        return {"domain": {"invoice_line_id": dom}}
