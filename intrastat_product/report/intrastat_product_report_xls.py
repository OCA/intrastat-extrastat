# Copyright 2009-2022 Noviat
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import _, models

from odoo.addons.report_xlsx_helper.report.report_xlsx_format import (
    FORMATS,
    XLS_HEADERS,
)

_logger = logging.getLogger(__name__)


IR_TRANSLATION_NAME = "intrastat.product.report"


class IntrastatProductDeclarationXlsx(models.AbstractModel):
    _name = "report.intrastat_product.product_declaration_xls"
    _inherit = "report.report_xlsx.abstract"
    _description = "Intrastat declaration"

    def _get_template(self, declaration):
        """
        Return a dictionary that contains columns specifications
        see: report_xlsx_helper / _write_line() method
        """

        template = {
            "product": {
                "header": {"type": "string", "value": _("Product")},
                "line": {
                    "value": self._render("line.product_id and line.product_id.name")
                },
                "width": 36,
            },
            "product_origin_country_code": {
                "header": {"type": "string", "value": _("Product C/O Code")},
                "line": {
                    "type": "string",
                    "value": self._render("line.product_origin_country_code or ''"),
                },
                "width": 10,
            },
            "product_origin_country": {
                "header": {"type": "string", "value": _("Product C/O")},
                "line": {
                    "type": "string",
                    "value": self._render("line.product_origin_country_id.name or ''"),
                },
                "width": 28,
            },
            "hs_code": {
                "header": {"type": "string", "value": _("Intrastat Code")},
                "line": {
                    "type": "string",
                    "value": self._render("line.hs_code_id.local_code"),
                },
                "width": 14,
            },
            "src_dest_country_code": {
                "header": {
                    "type": "string",
                    "value": _("Country Code of Origin/Destination"),
                },
                "line": {
                    "type": "string",
                    "value": self._render("line.src_dest_country_code"),
                },
                "width": 10,
            },
            "src_dest_country": {
                "header": {
                    "type": "string",
                    "value": _("Country of Origin/Destination"),
                },
                "line": {
                    "type": "string",
                    "value": self._render("line.src_dest_country_id.name"),
                },
                "width": 28,
            },
            "amount_company_currency": {
                "header": {
                    "type": "string",
                    "value": _("Fiscal Value"),
                    "format": FORMATS["format_theader_yellow_right"],
                },
                "line": {
                    "type": "number",
                    "value": self._render("line.amount_company_currency"),
                    "format": FORMATS["format_tcell_amount_right"],
                },
                "width": 18,
            },
            "accessory_cost": {
                "header": {
                    "type": "string",
                    "value": _("Accessory Costs"),
                    "format": FORMATS["format_theader_yellow_right"],
                },
                "line": {
                    "type": "number",
                    "value": self._render(
                        "line.amount_accessory_cost_company_currency"
                    ),
                    "format": FORMATS["format_tcell_amount_right"],
                },
                "width": 18,
            },
            "transaction_code": {
                "header": {
                    "type": "string",
                    "value": _("Intrastat Transaction Code"),
                },
                "line": {"value": self._render("line.transaction_id.code")},
                "width": 10,
            },
            "transaction": {
                "header": {"type": "string", "value": _("Intrastat Transaction")},
                "line": {"value": self._render("line.transaction_id.display_name")},
                "width": 36,
            },
            "weight": {
                "header": {
                    "type": "string",
                    "value": _("Weight"),
                    "format": FORMATS["format_theader_yellow_right"],
                },
                "line": {
                    "type": "number",
                    "value": self._render("line.weight"),
                    "format": FORMATS["format_tcell_amount_right"],
                },
                "width": 18,
            },
            "suppl_unit_qty": {
                "header": {
                    "type": "string",
                    "value": _("Suppl. Unit Qty"),
                    "format": FORMATS["format_theader_yellow_right"],
                },
                "line": {
                    # we don't specify a type here and rely on the
                    # report_xlsx_helper type detection to use
                    # write_string when suppl_unit_qty is zero
                    "value": self._render("line.suppl_unit_qty or ''"),
                    "format": FORMATS["format_tcell_amount_right"],
                },
                "width": 18,
            },
            "suppl_unit": {
                "header": {"type": "string", "value": _("Suppl. Unit")},
                "line": {"value": self._render("line.intrastat_unit_id.name or ''")},
                "width": 14,
            },
            "incoterm": {
                "header": {"type": "string", "value": _("Incoterm")},
                "line": {"value": self._render("line.incoterm_id.name or ''")},
                "width": 14,
            },
            "transport_code": {
                "header": {"type": "string", "value": _("Transport Mode Code")},
                "line": {"value": self._render("line.transport_id.code or ''")},
                "width": 10,
            },
            "transport": {
                "header": {"type": "string", "value": _("Transport Mode")},
                "line": {"value": self._render("line.transport_id.name or ''")},
                "width": 14,
            },
            "region": {
                "header": {"type": "string", "value": _("Intrastat Region")},
                "line": {"value": self._render("line.region_id.name or ''")},
                "width": 28,
            },
            "region_code": {
                "header": {"type": "string", "value": _("Intrastat Region Code")},
                "line": {"value": self._render("line.region_code or ''")},
                "width": 10,
            },
            "vat": {
                "header": {"type": "string", "value": _("VAT")},
                "line": {"value": self._render("line.vat or ''")},
                "width": 20,
            },
            "partner_id": {
                "header": {"type": "string", "value": _("Partner")},
                "line": {"value": self._render("line.partner_id.display_name or ''")},
                "width": 28,
            },
            "invoice": {
                "header": {"type": "string", "value": _("Invoice")},
                "line": {"value": self._render("line.invoice_id.name")},
                "width": 18,
            },
        }
        template.update(declaration._xls_template())

        return template

    def _get_ws_params(self, wb, data, declarations):
        template = self._get_template(declarations)
        res = []
        wanted_list_computation = declarations._xls_computation_line_fields()
        wanted_list_declaration = declarations._xls_declaration_line_fields()
        for declaration in declarations:
            dname = declaration.display_name
            res += [
                {
                    "ws_name": "%s %s" % (dname, _("comput.")),
                    "generate_ws_method": "_intrastat_report_computation",
                    "title": "%s : %s" % (dname, _("Computation Lines")),
                    "wanted_list": wanted_list_computation,
                    "col_specs": template,
                },
                {
                    "ws_name": "%s %s" % (dname, _("decl.")),
                    "generate_ws_method": "_intrastat_report_declaration",
                    "title": "%s : %s" % (dname, _("Declaration Lines")),
                    "wanted_list": wanted_list_declaration,
                    "col_specs": template,
                },
            ]
        return res

    def _report_title(self, ws, row_pos, ws_params, data, declaration):
        return self._write_ws_title(ws, row_pos, ws_params)

    def _empty_report(self, ws, row_pos, ws_params, data, declaration, report):
        if report == "computation":
            lines = _("Computation Lines")
        else:
            lines = _("Declaration Lines")
        no_entries = (
            _("No") + " " + lines + " " + _("for period %s") % declaration.year_month
        )
        ws.write_string(row_pos, 0, no_entries, FORMATS["format_left_bold"])

    def _intrastat_report_computation(self, workbook, ws, ws_params, data, declaration):
        report = "computation"
        lines = declaration.computation_line_ids
        self._intrastat_report(
            workbook, ws, ws_params, data, declaration, lines, report
        )

    def _intrastat_report_declaration(self, workbook, ws, ws_params, data, declaration):
        report = "declaration"
        lines = declaration.declaration_line_ids
        self._intrastat_report(
            workbook, ws, ws_params, data, declaration, lines, report
        )

    def _intrastat_report(
        self, workbook, ws, ws_params, data, declaration, lines, report
    ):
        ws.set_landscape()
        ws.fit_to_pages(1, 0)
        ws.set_header(XLS_HEADERS["xls_headers"]["standard"])
        ws.set_footer(XLS_HEADERS["xls_footers"]["standard"])

        self._set_column_width(ws, ws_params)

        row_pos = 0
        row_pos = self._report_title(ws, row_pos, ws_params, data, declaration)

        if not lines:
            return self._empty_report(ws, row_pos, ws_params, data, declaration, report)

        row_pos = self._write_line(
            ws,
            row_pos,
            ws_params,
            col_specs_section="header",
            default_format=FORMATS["format_theader_yellow_left"],
        )

        ws.freeze_panes(row_pos, 0)

        for line in lines:
            row_pos = self._write_line(
                ws,
                row_pos,
                ws_params,
                col_specs_section="line",
                render_space={"line": line},
                default_format=FORMATS["format_tcell_left"],
            )
