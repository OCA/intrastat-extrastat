# Copyright 2011-2017 Akretion France (http://www.akretion.com)
# Copyright 2009-2020 Noviat (http://www.noviat.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# @author Luc de Meyer <info@noviat.com>

import logging
from datetime import date, datetime

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import RedirectWarning, UserError, ValidationError

_logger = logging.getLogger(__name__)


class IntrastatProductDeclaration(models.Model):
    _name = "intrastat.product.declaration"
    _description = "Intrastat Product Report Base Object"
    _rec_name = "year_month"
    _inherit = ["mail.thread", "mail.activity.mixin", "intrastat.common"]
    _order = "year_month desc, type, revision"
    _sql_constraints = [
        (
            "date_uniq",
            "unique(year_month, company_id, type, revision)",
            "A declaration of the same type already exists for this month !"
            "\nYou should update the existing declaration "
            "or change the revision number of this one.",
        )
    ]
    # TODO:
    # drop the use of self._note & self._line_nbr when migrating to Odoo 14
    # refactoring this now may break the localisation modules
    _note = ""
    _line_nbr = ""

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        decl_date = fields.Date.context_today(self) - relativedelta(months=1)
        res.update(
            {"year": str(decl_date.year), "month": str(decl_date.month).rjust(2, "0")}
        )
        return res

    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        readonly=True,
        default=lambda self: self._default_company_id(),
    )
    company_country_code = fields.Char(
        compute="_compute_company_country_code",
        string="Company Country Code",
        readonly=True,
        store=True,
        help="Used in views and methods of localization modules.",
    )
    year = fields.Char(
        string="Year", required=True, states={"done": [("readonly", True)]}
    )
    month = fields.Selection(
        selection=[
            ("01", "01"),
            ("02", "02"),
            ("03", "03"),
            ("04", "04"),
            ("05", "05"),
            ("06", "06"),
            ("07", "07"),
            ("08", "08"),
            ("09", "09"),
            ("10", "10"),
            ("11", "11"),
            ("12", "12"),
        ],
        string="Month",
        required=True,
        states={"done": [("readonly", True)]},
    )
    year_month = fields.Char(
        compute="_compute_year_month",
        string="Period",
        readonly=True,
        tracking=True,
        store=True,
        help="Year and month of the declaration.",
    )
    type = fields.Selection(
        selection="_get_type",
        string="Type",
        required=True,
        states={"done": [("readonly", True)]},
        tracking=True,
        help="Select the declaration type.",
    )
    action = fields.Selection(
        selection="_get_action",
        string="Action",
        required=True,
        default="replace",
        states={"done": [("readonly", True)]},
        tracking=True,
    )
    revision = fields.Integer(
        string="Revision",
        default=1,
        states={"done": [("readonly", True)]},
        help="Used to keep track of changes",
    )
    computation_line_ids = fields.One2many(
        comodel_name="intrastat.product.computation.line",
        inverse_name="parent_id",
        string="Intrastat Product Computation Lines",
        states={"done": [("readonly", True)]},
    )
    declaration_line_ids = fields.One2many(
        comodel_name="intrastat.product.declaration.line",
        inverse_name="parent_id",
        string="Intrastat Product Declaration Lines",
        states={"done": [("readonly", True)]},
    )
    num_decl_lines = fields.Integer(
        compute="_compute_numbers",
        string="Number of Declaration Lines",
        store=True,
        tracking=True,
    )
    total_amount = fields.Integer(
        compute="_compute_numbers",
        string="Total Fiscal Amount",
        store=True,
        help="Total fiscal amount in company currency of the declaration.",
    )
    currency_id = fields.Many2one(
        "res.currency", related="company_id.currency_id", string="Currency"
    )
    state = fields.Selection(
        selection=[("draft", "Draft"), ("done", "Done")],
        string="State",
        readonly=True,
        tracking=True,
        copy=False,
        default="draft",
        help="State of the declaration. When the state is set to 'Done', "
        "the parameters become read-only.",
    )
    note = fields.Text(
        string="Notes", help="You can add some comments here if you want."
    )
    reporting_level = fields.Selection(
        selection="_get_reporting_level",
        string="Reporting Level",
        states={"done": [("readonly", True)]},
    )
    valid = fields.Boolean(compute="_compute_check_validity", string="Valid")
    xml_attachment_id = fields.Many2one("ir.attachment", string="XML Export")

    @api.model
    def _default_company_id(self):
        return self.env.company

    @api.model
    def _get_type(self):
        res = []
        company = self.env.user.company_id
        arrivals = company.intrastat_arrivals
        dispatches = company.intrastat_dispatches
        if arrivals != "exempt":
            res.append(("arrivals", _("Declaration for Arrivals")))
        if dispatches != "exempt":
            res.append(("dispatches", _("Declaration for Dispatches")))
        return res

    @api.model
    def _get_reporting_level(self):
        return [("standard", _("Standard")), ("extended", _("Extended"))]

    @api.model
    def _get_action(self):
        return [
            ("replace", _("Replace")),
            ("append", _("Append")),
            ("nihil", _("Nihil")),
        ]

    @api.depends("company_id")
    def _compute_company_country_code(self):
        for this in self:
            if this.company_id:
                if not this.company_id.country_id:
                    raise ValidationError(_("You must set company's country !"))
                this.company_country_code = this.company_id.country_id.code.lower()

    @api.depends("year", "month")
    def _compute_year_month(self):
        for this in self:
            if this.year and this.month:
                this.year_month = "-".join([this.year, this.month])

    @api.depends("month")
    def _compute_check_validity(self):
        """ TO DO: logic based upon computation lines """
        for this in self:
            this.valid = True

    @api.model
    @api.constrains("year")
    def _check_year(self):
        for this in self:
            if len(this.year) != 4 or this.year[0] != "2":
                raise ValidationError(_("Invalid Year !"))

    @api.onchange("type")
    def _onchange_type(self):
        if self.type == "arrivals":
            self.reporting_level = (
                self.company_id.intrastat_arrivals == "extended"
                and "extended"
                or "standard"
            )
        if self.type == "dispatches":
            self.reporting_level = (
                self.company_id.intrastat_dispatches == "extended"
                and "extended"
                or "standard"
            )

    def copy(self, default=None):
        self.ensure_one()
        default = default or {}
        default["revision"] = self.revision + 1
        return super().copy(default)

    def _account_config_warning(self, msg):
        action = self.env.ref("account.action_account_config")
        raise RedirectWarning(
            msg, action.id, _("Go to Accounting Configuration Settings screen")
        )

    def _get_partner_country(self, inv_line):
        country = (
            inv_line.move_id.src_dest_country_id
            or inv_line.move_id.partner_id.country_id
        )
        if not country.intrastat:
            country = False
        elif country == self.company_id.country_id:
            country = False
        return country

    def _get_intrastat_transaction(self, inv_line):
        invoice = inv_line.move_id
        if invoice.intrastat_transaction_id:
            return invoice.intrastat_transaction_id
        else:
            company = invoice.company_id
            if invoice.type == "out_invoice":
                return company.intrastat_transaction_out_invoice
            elif invoice.type == "out_refund":
                return company.intrastat_transaction_out_refund
            elif invoice.type == "in_invoice":
                return company.intrastat_transaction_in_invoice
            elif invoice.type == "in_refund":
                return company.intrastat_transaction_in_refund

    def _get_weight_and_supplunits(self, inv_line, hs_code):
        line_nbr = self._line_nbr
        line_qty = inv_line.quantity
        product = inv_line.product_id
        intrastat_unit_id = hs_code.intrastat_unit_id
        source_uom = inv_line.product_uom_id
        weight_uom_categ = self._get_uom_refs("weight_uom_categ")
        kg_uom = self._get_uom_refs("kg_uom")
        pce_uom_categ = self._get_uom_refs("pce_uom_categ")
        pce_uom = self._get_uom_refs("pce_uom")
        weight = suppl_unit_qty = 0.0

        if not source_uom:
            line_notes = [_("Missing unit of measure.")]
            self._note += self._format_line_note(inv_line, line_nbr, line_notes)
            return weight, suppl_unit_qty

        if intrastat_unit_id:
            target_uom = intrastat_unit_id.uom_id
            if not target_uom:
                line_notes = [
                    _("Intrastat Code %s:") % hs_code.display_name,
                    _(
                        "Conversion from Intrastat Supplementary Unit '%s' to "
                        "Unit of Measure is not implemented yet."
                    )
                    % intrastat_unit_id.name,
                ]
                self._note += self._format_line_note(inv_line, line_nbr, line_notes)
                return weight, suppl_unit_qty
            if target_uom.category_id == source_uom.category_id:
                suppl_unit_qty = source_uom._compute_quantity(line_qty, target_uom)
            else:
                line_notes = [
                    _(
                        "Conversion from unit of measure '%s' to '%s' "
                        "is not implemented yet."
                    )
                    % (source_uom.name, target_uom.name)
                ]
                self._note += self._format_line_note(inv_line, line_nbr, line_notes)
                return weight, suppl_unit_qty

        if weight:
            return weight, suppl_unit_qty

        if source_uom == kg_uom:
            weight = line_qty
        elif source_uom.category_id == weight_uom_categ:
            weight = source_uom._compute_quantity(line_qty, kg_uom)
        elif source_uom.category_id == pce_uom_categ:
            if not product.weight:  # re-create weight_net ?
                line_notes = [
                    _("Missing weight on product %s.") % product.name_get()[0][1]
                ]
                self._note += self._format_line_note(inv_line, line_nbr, line_notes)
                return weight, suppl_unit_qty
            if source_uom == pce_uom:
                weight = product.weight * line_qty  # product.weight_net
            else:
                # Here, I suppose that, on the product, the
                # weight is per PCE and not per uom_id
                # product.weight_net
                weight = product.weight * source_uom._compute_quantity(
                    line_qty, pce_uom
                )
        else:
            line_notes = [
                _(
                    "Conversion from unit of measure '%s' to 'Kg' "
                    "is not implemented yet. It is needed for product '%s'."
                )
                % (source_uom.name, product.name_get()[0][1])
            ]
            self._note += self._format_line_note(inv_line, line_nbr, line_notes)
            return weight, suppl_unit_qty

        return weight, suppl_unit_qty

    def _get_amount(self, inv_line):
        invoice = inv_line.move_id
        amount = invoice.currency_id._convert(
            inv_line.price_subtotal,
            self.company_id.currency_id,
            self.company_id,
            invoice.date,
        )
        return amount

    def _get_region(self, inv_line):
        """
        For supplier invoices/refunds: if the invoice line is linked
        to a stock move, use the destination stock location ;
        otherwise, get the PO (which is linked to a stock location)
        and then get the warehouse.
        It is important to take into account the following scenario:
        I order a qty of 50 kg and my suppliers delivers and invoices 52 kg
        (quite common in some industries where the order qty cannot be exact
        due to some operational constraints) ; in this case, I have a qty of
        2 kg which is not linked to a PO, but it is linked to a stock move.

        For customer invoices/refunds: if the invoice line is linked to a
        stock move, use the source stock location ;
        otherwise, get the sale order, which is linked to the warehouse.

        If none found, get the company's default intrastat region.

        """
        region = False
        inv_type = inv_line.move_id.type
        if inv_type in ("in_invoice", "in_refund"):
            po_lines = self.env["purchase.order.line"].search(
                [("invoice_lines", "in", inv_line.id)]
            )
            if po_lines:
                if po_lines[0].move_ids:
                    region = (
                        po_lines[0].move_ids[0].location_dest_id.get_intrastat_region()
                    )
        elif inv_type in ("out_invoice", "out_refund"):
            so_lines = self.env["sale.order.line"].search(
                [("invoice_lines", "in", inv_line.id)]
            )
            if so_lines:
                so = so_lines[0].order_id
                region = so.warehouse_id.region_id
        if not region:
            if self.company_id.intrastat_region_id:
                region = self.company_id.intrastat_region_id
        return region

    def _get_transport(self, inv_line):
        transport = (
            inv_line.move_id.intrastat_transport_id
            or self.company_id.intrastat_transport_id
        )
        if not transport:
            msg = _(
                "The default Intrastat Transport Mode "
                "of the Company is not set, "
                "please configure it first."
            )
            self._account_config_warning(msg)
        return transport

    def _get_incoterm(self, inv_line):
        incoterm = inv_line.move_id.invoice_incoterm_id or self.company_id.incoterm_id
        if not incoterm:
            msg = _(
                "The default Incoterm "
                "of the Company is not set, "
                "please configure it first."
            )
            self._account_config_warning(msg)
        return incoterm

    def _get_product_origin_country(self, inv_line):
        return inv_line.product_id.origin_country_id

    def _update_computation_line_vals(self, inv_line, line_vals):
        """ placeholder for localization modules """
        pass

    def _handle_invoice_accessory_cost(
        self,
        invoice,
        lines_current_invoice,
        total_inv_accessory_costs_cc,
        total_inv_product_cc,
        total_inv_weight,
    ):
        """
        Affect accessory costs pro-rata of the value
        (or pro-rata of the weight if the goods of the invoice
        have no value)

        This method allows to implement a different logic
        in the localization modules.
        E.g. in Belgium accessory cost should not be added.
        """
        if total_inv_accessory_costs_cc:
            if total_inv_product_cc:
                # pro-rata of the value
                for ac_line_vals in lines_current_invoice:
                    ac_line_vals["amount_accessory_cost_company_currency"] = (
                        total_inv_accessory_costs_cc
                        * ac_line_vals["amount_company_currency"]
                        / total_inv_product_cc
                    )
            elif total_inv_weight:
                # pro-rata of the weight
                for ac_line_vals in lines_current_invoice:
                    ac_line_vals["amount_accessory_cost_company_currency"] = (
                        total_inv_accessory_costs_cc
                        * ac_line_vals["weight"]
                        / total_inv_weight
                    )
            else:
                for ac_line_vals in lines_current_invoice:
                    ac_line_vals[
                        "amount_accessory_cost_company_currency"
                    ] = total_inv_accessory_costs_cc / len(lines_current_invoice)

    def _prepare_invoice_domain(self):
        """
        Complete this method in the localization module
        with the country-specific logic for arrivals and dispatches.
        Cf. l10n_be_intrastat_product_declaration for an example
        The dates are based on account.move,date in stead of invoice_date
        to ensure consistency between intrastat and intracomm tax declaration.
        """
        start_date = date(int(self.year), int(self.month), 1)
        end_date = start_date + relativedelta(day=1, months=+1, days=-1)
        domain = [
            ("date", ">=", start_date),
            ("date", "<=", end_date),
            ("state", "=", "posted"),
            ("intrastat_country", "=", True),
            ("company_id", "=", self.company_id.id),
            ("type", "!=", "entry"),
        ]
        return domain

    def _is_product(self, invoice_line):
        if invoice_line.product_id and invoice_line.product_id.type in (
            "product",
            "consu",
        ):
            return True
        else:
            return False

    def _gather_invoices_init(self):
        """ placeholder for localization modules """
        pass

    def _format_line_note(self, line, line_nbr, line_notes):
        indent = 8 * " "
        note = _("Invoice %s, line %s") % (line.move_id.name, line_nbr)
        note += ":\n"
        for line_note in line_notes:
            note += indent + line_note
            note += "\n"
        return note

    def _gather_invoices(self):

        lines = []
        accessory_costs = self.company_id.intrastat_accessory_costs

        self._gather_invoices_init()
        domain = self._prepare_invoice_domain()
        order = "journal_id, name"
        invoices = self.env["account.move"].search(domain, order=order)

        for invoice in invoices:

            lines_current_invoice = []
            total_inv_accessory_costs_cc = 0.0  # in company currency
            total_inv_product_cc = 0.0  # in company currency
            total_inv_weight = 0.0
            for line_nbr, inv_line in enumerate(invoice.invoice_line_ids, start=1):
                self._line_nbr = line_nbr
                inv_intrastat_line = invoice.intrastat_line_ids.filtered(
                    lambda r: r.invoice_line_id == inv_line
                )

                if (
                    accessory_costs
                    and inv_line.product_id
                    and inv_line.product_id.is_accessory_cost
                ):
                    acost = invoice.currency_id._convert(
                        inv_line.price_subtotal,
                        self.company_id.currency_id,
                        self.company_id,
                        invoice.date,
                    )
                    total_inv_accessory_costs_cc += acost

                    continue

                if not inv_line.quantity:
                    _logger.info(
                        "Skipping invoice line %s qty %s "
                        "of invoice %s. Reason: qty = 0"
                        % (inv_line.name, inv_line.quantity, invoice.name)
                    )
                    continue

                partner_country = self._get_partner_country(inv_line)
                if not partner_country:
                    _logger.info(
                        "Skipping invoice line %s qty %s "
                        "of invoice %s. Reason: no partner_country"
                        % (inv_line.name, inv_line.quantity, invoice.name)
                    )
                    continue

                if any(
                    [tax.exclude_from_intrastat_if_present for tax in inv_line.tax_ids]
                ):
                    _logger.info(
                        "Skipping invoice line %s "
                        "qty %s of invoice %s. Reason: "
                        "tax.exclude_from_intrastat_if_present"
                        % (inv_line.name, inv_line.quantity, invoice.name)
                    )
                    continue

                if inv_intrastat_line:
                    hs_code = inv_intrastat_line.hs_code_id
                elif inv_line.product_id and self._is_product(inv_line):
                    hs_code = inv_line.product_id.get_hs_code_recursively()
                    if not hs_code:
                        line_notes = [
                            _("Missing Intrastat Code on product %s. ")
                            % (inv_line.product_id.name_get()[0][1])
                        ]
                        self._note += self._format_line_note(
                            inv_line, line_nbr, line_notes
                        )
                        continue
                else:
                    _logger.info(
                        "Skipping invoice line %s qty %s "
                        "of invoice %s. Reason: no product nor Intrastat Code"
                        % (inv_line.name, inv_line.quantity, invoice.name)
                    )
                    continue

                intrastat_transaction = self._get_intrastat_transaction(inv_line)

                if inv_intrastat_line:
                    weight = inv_intrastat_line.transaction_weight
                    suppl_unit_qty = inv_intrastat_line.transaction_suppl_unit_qty
                else:
                    weight, suppl_unit_qty = self._get_weight_and_supplunits(
                        inv_line, hs_code
                    )
                total_inv_weight += weight

                amount_company_currency = self._get_amount(inv_line)
                total_inv_product_cc += amount_company_currency

                if inv_intrastat_line:
                    product_origin_country = (
                        inv_intrastat_line.product_origin_country_id
                    )
                else:
                    product_origin_country = self._get_product_origin_country(inv_line)

                region = self._get_region(inv_line)

                line_vals = {
                    "parent_id": self.id,
                    "invoice_line_id": inv_line.id,
                    "src_dest_country_id": partner_country.id,
                    "product_id": inv_line.product_id.id,
                    "hs_code_id": hs_code.id,
                    "weight": weight,
                    "suppl_unit_qty": suppl_unit_qty,
                    "amount_company_currency": amount_company_currency,
                    "amount_accessory_cost_company_currency": 0.0,
                    "transaction_id": intrastat_transaction.id,
                    "product_origin_country_id": product_origin_country.id or False,
                    "region_id": region and region.id or False,
                }

                # extended declaration
                if self._extended:
                    transport = self._get_transport(inv_line)
                    line_vals.update({"transport_id": transport.id})

                self._update_computation_line_vals(inv_line, line_vals)

                if line_vals:
                    lines_current_invoice.append(line_vals)

            self._handle_invoice_accessory_cost(
                invoice,
                lines_current_invoice,
                total_inv_accessory_costs_cc,
                total_inv_product_cc,
                total_inv_weight,
            )

            for line_vals in lines_current_invoice:
                if (
                    not line_vals["amount_company_currency"]
                    and not line_vals["amount_accessory_cost_company_currency"]
                ):
                    inv_line = self.env["account.move.line"].browse(
                        line_vals["invoice_line_id"]
                    )
                    _logger.info(
                        "Skipping invoice line %s qty %s "
                        "of invoice %s. Reason: price_subtotal = 0 "
                        "and accessory costs = 0"
                        % (inv_line.name, inv_line.quantity, inv_line.move_id.name)
                    )
                    continue
                lines.append(line_vals)

        return lines

    def _get_uom_refs(self, ref):
        uom_refs = {
            "weight_uom_categ": self.env.ref("uom.product_uom_categ_kgm"),
            "kg_uom": self.env.ref("uom.product_uom_kgm"),
            "pce_uom_categ": self.env.ref("uom.product_uom_categ_unit"),
            "pce_uom": self.env.ref("uom.product_uom_unit"),
        }
        return uom_refs[ref]

    def action_gather(self):
        self.ensure_one()
        self.message_post(body=_("Generate Lines from Invoices"))
        self._check_generate_lines()
        self._note = ""
        if (
            self.type == "arrivals" and self.company_id.intrastat_arrivals == "extended"
        ) or (
            self.type == "dispatches"
            and self.company_id.intrastat_dispatches == "extended"
        ):
            self._extended = True
        else:
            self._extended = False

        self.computation_line_ids.unlink()
        self.declaration_line_ids.unlink()
        lines = self._gather_invoices()

        if not lines:
            self.action = "nihil"
            note = (
                "\n"
                + _("No records found for the selected period !")
                + "\n"
                + _("The Declaration Action has been set to 'nihil'.")
            )
            self._note += note
        else:
            self.write({"computation_line_ids": [(0, 0, x) for x in lines]})

        if self._note:
            note_header = (
                "\n\n>>> "
                + fields.Datetime.to_string(
                    fields.Datetime.context_timestamp(self, datetime.now())
                )
                + "\n"
            )
            self.note = note_header + self._note + (self.note or "")
            result_view = self.env.ref("intrastat_base.intrastat_result_view_form")
            return {
                "name": _("Generate lines from invoices: results"),
                "view_type": "form",
                "view_mode": "form",
                "res_model": "intrastat.result.view",
                "view_id": result_view.id,
                "target": "new",
                "context": dict(self._context, note=self._note),
                "type": "ir.actions.act_window",
            }

        return True

    @api.model
    def _group_line_hashcode_fields(self, computation_line):
        return {
            "country": computation_line.src_dest_country_id.id or False,
            "hs_code_id": computation_line.hs_code_id.id or False,
            "intrastat_unit": computation_line.intrastat_unit_id.id or False,
            "transaction": computation_line.transaction_id.id or False,
            "transport": computation_line.transport_id.id or False,
            "region": computation_line.region_id.id or False,
            "product_origin_country": computation_line.product_origin_country_id.id
            or False,
        }

    def group_line_hashcode(self, computation_line):
        hc_fields = self._group_line_hashcode_fields(computation_line)
        hashcode = "-".join([str(f) for f in hc_fields.values()])
        return hashcode

    @api.model
    def _prepare_grouped_fields(self, computation_line, fields_to_sum):
        vals = {
            "src_dest_country_id": computation_line.src_dest_country_id.id,
            "intrastat_unit_id": computation_line.intrastat_unit_id.id,
            "hs_code_id": computation_line.hs_code_id.id,
            "transaction_id": computation_line.transaction_id.id,
            "transport_id": computation_line.transport_id.id,
            "region_id": computation_line.region_id.id,
            "parent_id": computation_line.parent_id.id,
            "product_origin_country_id": computation_line.product_origin_country_id.id,
            "amount_company_currency": 0.0,
        }
        for field in fields_to_sum:
            vals[field] = 0.0
        return vals

    def _fields_to_sum(self):
        fields_to_sum = ["weight", "suppl_unit_qty"]
        return fields_to_sum

    @api.model
    def _prepare_declaration_line(self, computation_lines):
        fields_to_sum = self._fields_to_sum()
        vals = self._prepare_grouped_fields(computation_lines[0], fields_to_sum)
        for computation_line in computation_lines:
            for field in fields_to_sum:
                vals[field] += computation_line[field]
            vals["amount_company_currency"] += (
                computation_line["amount_company_currency"]
                + computation_line["amount_accessory_cost_company_currency"]
            )
        # round, otherwise odoo with truncate (6.7 -> 6... instead of 7 !)
        for field in fields_to_sum:
            vals[field] = int(round(vals[field]))
        if not vals["weight"]:
            vals["weight"] = 1
        vals["amount_company_currency"] = int(round(vals["amount_company_currency"]))
        return vals

    def generate_declaration(self):
        """ generate declaration lines """
        self.ensure_one()
        assert self.valid, "Computation lines are not valid"
        self.message_post(body=_("Generate Declaration Lines"))
        # Delete existing declaration lines
        self.declaration_line_ids.unlink()
        # Regenerate declaration lines from computation lines
        dl_group = {}
        for cl in self.computation_line_ids:
            hashcode = self.group_line_hashcode(cl)
            if hashcode in dl_group:
                dl_group[hashcode].append(cl)
            else:
                dl_group[hashcode] = [cl]
        ipdl = self.declaration_line_ids
        for cl_lines in list(dl_group.values()):
            vals = self._prepare_declaration_line(cl_lines)
            declaration_line = ipdl.create(vals)
            for cl in cl_lines:
                cl.write({"declaration_line_id": declaration_line.id})
        return True

    def generate_xml(self):
        """ generate the INTRASTAT Declaration XML file """
        self.ensure_one()
        if self.xml_attachment_id:
            raise UserError(
                _(
                    "An XML Export already exists for %s. "
                    "To re-generate it, you must first delete it."
                )
                % self.display_name
            )
        self.message_post(body=_("Generate XML Declaration File"))
        self._check_generate_xml()
        self._unlink_attachments()
        xml_string = self._generate_xml()
        if xml_string:
            attach_id = self._attach_xml_file(
                xml_string, "{}_{}".format(self.type, self.revision)
            )
            self.write({"xml_attachment_id": attach_id})
            return self._open_attach_view(attach_id)
        else:
            raise UserError(_("No XML File has been generated."))

    def create_xls(self):
        if self.env.context.get("computation_lines"):
            report_file = "instrastat_transactions"
        else:
            report_file = "instrastat_declaration_lines"
        return {
            "type": "ir.actions.report",
            "report_type": "xlsx",
            "report_name": "intrastat_product.product_declaration_xls",
            "context": dict(self.env.context, report_file=report_file),
            "data": {"dynamic_report": True},
        }

    @api.model
    def _xls_computation_line_fields(self):
        """
        Update list in custom module to add/drop columns or change order
        """
        return [
            "product",
            "product_origin_country",
            "hs_code",
            "src_dest_country",
            "amount_company_currency",
            "accessory_cost",
            "transaction",
            "weight",
            "suppl_unit_qty",
            "suppl_unit",
            "transport",
            "invoice",
        ]

    @api.model
    def _xls_declaration_line_fields(self):
        """
        Update list in custom module to add/drop columns or change order
        """
        return [
            "hs_code",
            "src_dest_country",
            "amount_company_currency",
            "transaction",
            "weight",
            "suppl_unit_qty",
            "suppl_unit",
            "transport",
        ]

    @api.model
    def _xls_template(self):
        """
        Placeholder for excel report template updates

        """
        return {}

    def done(self):
        self.write({"state": "done"})

    def back2draft(self):
        self.write({"state": "draft"})


class IntrastatProductComputationLine(models.Model):
    _name = "intrastat.product.computation.line"
    _description = "Intrastat Product Computataion Lines"

    parent_id = fields.Many2one(
        "intrastat.product.declaration",
        string="Intrastat Product Declaration",
        ondelete="cascade",
        readonly=True,
    )
    company_id = fields.Many2one(related="parent_id.company_id")
    company_currency_id = fields.Many2one(
        related="company_id.currency_id", string="Company currency"
    )
    type = fields.Selection(related="parent_id.type")
    reporting_level = fields.Selection(related="parent_id.reporting_level")
    valid = fields.Boolean(compute="_compute_check_validity", string="Valid")
    invoice_line_id = fields.Many2one(
        "account.move.line", string="Invoice Line", readonly=True
    )
    invoice_id = fields.Many2one(
        "account.move", related="invoice_line_id.move_id", string="Invoice"
    )
    declaration_line_id = fields.Many2one(
        "intrastat.product.declaration.line", string="Declaration Line", readonly=True
    )
    src_dest_country_id = fields.Many2one(
        "res.country",
        string="Country",
        help="Country of Origin/Destination",
        domain=[("intrastat", "=", True)],
    )
    product_id = fields.Many2one(
        "product.product", related="invoice_line_id.product_id"
    )
    hs_code_id = fields.Many2one("hs.code", string="Intrastat Code")
    intrastat_unit_id = fields.Many2one(
        "intrastat.unit",
        related="hs_code_id.intrastat_unit_id",
        string="Suppl. Unit",
        help="Intrastat Supplementary Unit",
    )
    weight = fields.Float(
        string="Weight", digits="Stock Weight", help="Net weight in Kg"
    )
    suppl_unit_qty = fields.Float(
        string="Suppl. Unit Qty",
        digits="Product Unit of Measure",
        help="Supplementary Units Quantity",
    )
    amount_company_currency = fields.Float(
        string="Fiscal Value",
        digits="Account",
        required=True,
        help="Amount in company currency to write in the declaration. "
        "Amount in company currency = amount in invoice currency "
        "converted to company currency with the rate of the invoice date.",
    )
    amount_accessory_cost_company_currency = fields.Float(
        string="Accessory Costs",
        digits="Account",
        help="Amount in company currency of the accessory costs related to "
        "this invoice line (by default, these accessory costs are computed "
        "at the pro-rata of the amount of each invoice line.",
    )
    transaction_id = fields.Many2one(
        "intrastat.transaction", string="Intrastat Transaction"
    )
    region_id = fields.Many2one("intrastat.region", string="Intrastat Region")
    # extended declaration
    incoterm_id = fields.Many2one("account.incoterms", string="Incoterm")
    transport_id = fields.Many2one("intrastat.transport_mode", string="Transport Mode")
    product_origin_country_id = fields.Many2one(
        "res.country",
        string="Country of Origin of the Product",
        help="Country of origin of the product i.e. product 'made in ____'",
    )

    @api.depends("transport_id")
    def _compute_check_validity(self):
        """ TO DO: logic based upon fields """
        for this in self:
            this.valid = True

    # TODO: product_id is a readonly related field 'invoice_line_id.product_id'
    # so the onchange is non-sense. Either we convert product_id to a regular
    # field or we keep it a related field and we remove this onchange
    @api.onchange("product_id")
    def _onchange_product(self):
        self.weight = 0.0
        self.suppl_unit_qty = 0.0
        self.intrastat_code_id = False
        self.intrastat_unit_id = False
        if self.product_id:
            self.intrastat_code_id = self.product_id.intrastat_id
            self.intrastat_unit_id = self.product_id.intrastat_id.intrastat_unit_id
            if not self.intrastat_unit_id:
                self.weight = self.product_id.weight


class IntrastatProductDeclarationLine(models.Model):
    _name = "intrastat.product.declaration.line"
    _description = "Intrastat Product Declaration Lines"

    parent_id = fields.Many2one(
        "intrastat.product.declaration",
        string="Intrastat Product Declaration",
        ondelete="cascade",
        readonly=True,
    )
    company_id = fields.Many2one(related="parent_id.company_id")
    company_currency_id = fields.Many2one(
        related="company_id.currency_id", string="Company currency"
    )
    type = fields.Selection(related="parent_id.type")
    reporting_level = fields.Selection(related="parent_id.reporting_level")
    computation_line_ids = fields.One2many(
        "intrastat.product.computation.line",
        "declaration_line_id",
        string="Computation Lines",
        readonly=True,
    )
    src_dest_country_id = fields.Many2one(
        "res.country",
        string="Country",
        help="Country of Origin/Destination",
        domain=[("intrastat", "=", True)],
    )
    hs_code_id = fields.Many2one("hs.code", string="Intrastat Code")
    intrastat_unit_id = fields.Many2one(
        "intrastat.unit",
        related="hs_code_id.intrastat_unit_id",
        string="Suppl. Unit",
        help="Intrastat Supplementary Unit",
    )
    weight = fields.Integer(string="Weight", help="Net weight in Kg")
    suppl_unit_qty = fields.Integer(
        string="Suppl. Unit Qty", help="Supplementary Units Quantity"
    )
    amount_company_currency = fields.Integer(
        string="Fiscal Value",
        help="Amount in company currency to write in the declaration. "
        "Amount in company currency = amount in invoice currency "
        "converted to company currency with the rate of the invoice date.",
    )
    transaction_id = fields.Many2one(
        "intrastat.transaction", string="Intrastat Transaction"
    )
    region_id = fields.Many2one("intrastat.region", string="Intrastat Region")
    # extended declaration
    incoterm_id = fields.Many2one("account.incoterms", string="Incoterm")
    transport_id = fields.Many2one("intrastat.transport_mode", string="Transport Mode")
    product_origin_country_id = fields.Many2one(
        "res.country",
        string="Country of Origin of the Product",
        help="Country of origin of the product i.e. product 'made in ____'",
    )
