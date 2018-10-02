# -*- coding: utf-8 -*-
# Copyright 2009-2018 Noviat
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo.addons.report_xlsx_helper.report.abstract_report_xlsx \
    import AbstractReportXlsx
from odoo.report import report_sxw
from odoo.tools.translate import translate, _

_logger = logging.getLogger(__name__)


IR_TRANSLATION_NAME = 'intrastat.product.report'


class IntrastatProductDeclarationXlsx(AbstractReportXlsx):

    def _(self, src):
        lang = self.env.context.get('lang', 'en_US')
        val = translate(
            self.env.cr, IR_TRANSLATION_NAME, 'report', lang, src) or src
        return val

    def _get_template(self):

        template = {
            'product': {
                'header': {
                    'type': 'string',
                    'value': self._('Product'),
                },
                'line': {
                    'value': self._render(
                        "line.product_id and line.product_id.name"),
                },
                'width': 36,
            },
            'product_origin_country': {
                'header': {
                    'type': 'string',
                    'value': self._('Country of Origin of the Product'),
                },
                'line': {
                    'type': 'string',
                    'value': self._render(
                        "line.product_origin_country_id.name or ''"),
                },
                'width': 28,
            },
            'hs_code': {
                'header': {
                    'type': 'string',
                    'value': self._('Intrastat Code'),
                },
                'line': {
                    'type': 'string',
                    'value': self._render(
                        "line.hs_code_id.local_code"),
                },
                'width': 14,
            },
            'src_dest_country': {
                'header': {
                    'type': 'string',
                    'value': self._('Country of Origin/Destination'),
                },
                'line': {
                    'type': 'string',
                    'value': self._render(
                        "line.src_dest_country_id.name"),
                },
                'width': 28,
            },
            'amount_company_currency': {
                'header': {
                    'type': 'string',
                    'value': self._('Fiscal Value'),
                    'format': self.format_theader_yellow_right,
                },
                'line': {
                    'type': 'number',
                    'value': self._render("line.amount_company_currency"),
                    'format': self.format_tcell_amount_right,
                },
                'width': 18,
            },
            'accessory_cost': {
                'header': {
                    'type': 'string',
                    'value': self._('Accessory Costs'),
                    'format': self.format_theader_yellow_right,
                },
                'line': {
                    'type': 'number',
                    'value': self._render(
                        "line.amount_accessory_cost_company_currency"),
                    'format': self.format_tcell_amount_right,
                },
                'width': 18,
            },
            'transaction': {
                'header': {
                    'type': 'string',
                    'value': self._('Intrastat Transaction'),
                },
                'line': {
                    'value': self._render(
                        "line.transaction_id.display_name"),
                },
                'width': 36,
            },
            'weight': {
                'header': {
                    'type': 'string',
                    'value': self._('Weight'),
                    'format': self.format_theader_yellow_right,
                },
                'line': {
                    'type': 'number',
                    'value': self._render(
                        "line.weight"),
                    'format': self.format_tcell_amount_right,
                },
                'width': 18,
            },
            'suppl_unit_qty': {
                'header': {
                    'type': 'string',
                    'value': self._('Suppl. Unit Qty'),
                    'format': self.format_theader_yellow_right,
                },
                'line': {
                    # we don't specify a type here and rely on the
                    # report_xlsx_helper type detection to use
                    # write_string when suppl_unit_qty is zero
                    'value': self._render(
                        "line.suppl_unit_qty or ''"),
                    'format': self.format_tcell_amount_right,
                },
                'width': 18,
            },
            'suppl_unit': {
                'header': {
                    'type': 'string',
                    'value': self._('Suppl. Unit'),
                },
                'line': {
                    'value': self._render(
                        "line.intrastat_unit_id.name or ''"),
                },
                'width': 14,
            },
            'incoterm': {
                'header': {
                    'type': 'string',
                    'value': self._('Incoterm'),
                },
                'line': {
                    'value': self._render("line.incoterm_id.name or ''"),
                },
                'width': 14,
            },
            'transport': {
                'header': {
                    'type': 'string',
                    'value': self._('Transport Mode'),
                },
                'line': {
                    'value': self._render("line.transport_id.name or ''"),
                },
                'width': 14,
            },
            'region': {
                'header': {
                    'type': 'string',
                    'value': self._('Intrastat Region'),
                },
                'line': {
                    'value': self._render("line.region_id.name or ''"),
                },
                'width': 28,
            },
            'invoice': {
                'header': {
                    'type': 'string',
                    'value': self._('Invoice'),
                },
                'line': {
                    'value': self._render("line.invoice_id.number"),
                },
                'width': 18,
            },
        }
        template.update(
            self.env['intrastat.product.declaration']._xls_template())

        return template

    def getObjects(self, cr, uid, ids, context):
        """
        Adapt logic since localization modules have other
        object tables than the object on which this report is defined.
        """
        active_model = self.env.context['active_model']
        active_id = self.env.context['active_id']
        declaration = self.env[active_model].browse(active_id)
        return declaration

    def _get_ws_params(self, wb, data, declaration):
        template = self._get_template()
        if self.env.context.get('computation_lines'):
            wl = declaration._xls_computation_line_fields()
            report = 'computation'
        else:
            wl = declaration._xls_declaration_line_fields()
            report = 'declaration'

        title = self._get_title(declaration, report, format='normal')
        title_short = self._get_title(declaration, report, format='short')
        sheet_name = title_short[:31].replace('/', '-')

        params = {
            'ws_name': sheet_name,
            'generate_ws_method': '_intrastat_report',
            'title': title,
            'wanted_list': wl,
            'col_specs': template,
        }
        return [params]

    def _get_title(self, declaration, report, format='normal'):
        title = declaration.year_month
        if format == 'normal':
            if report == 'computation':
                title += ' : ' + _('Computation Lines')
            else:
                title += ' : ' + _('Declaration Lines')
        return title

    def _report_title(self, ws, row_pos, ws_params, data, declaration):
        return self._write_ws_title(ws, row_pos, ws_params)

    def _empty_report(self, ws, row_pos, ws_params, data, declaration,
                      report):
        if report == 'computation':
            lines = _('Computation Lines')
        else:
            lines = _('Declaration Lines')
        no_entries = _("No") + " " + lines + " " + _("for period %s") \
            % declaration.year_month
        ws.write_string(row_pos, 0, no_entries, self.format_left_bold)

    def _intrastat_report(self, workbook, ws, ws_params, data, declaration):

        ws.set_landscape()
        ws.fit_to_pages(1, 0)
        ws.set_header(self.xls_headers['standard'])
        ws.set_footer(self.xls_footers['standard'])

        self._set_column_width(ws, ws_params)

        row_pos = 0
        row_pos = self._report_title(ws, row_pos, ws_params, data, declaration)

        if self.env.context.get('computation_lines'):
            report = 'computation'
            lines = declaration.computation_line_ids
        else:
            report = 'declaration'
            lines = declaration.declaration_line_ids

        if not lines:
            return self._empty_report(
                ws, row_pos, ws_params, data, declaration, report)

        row_pos = self._write_line(
            ws, row_pos, ws_params, col_specs_section='header',
            default_format=self.format_theader_yellow_left)

        ws.freeze_panes(row_pos, 0)

        for line in lines:
            row_pos = self._write_line(
                ws, row_pos, ws_params, col_specs_section='line',
                render_space={'line': line},
                default_format=self.format_tcell_left)


IntrastatProductDeclarationXlsx(
    'report.intrastat.product.declaration.xlsx',
    'intrastat.product.declaration',
    parser=report_sxw.rml_parse)
