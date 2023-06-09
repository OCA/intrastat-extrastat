# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import xlrd
from werkzeug.urls import url_encode

from odoo.addons.intrastat_base.tests.common import IntrastatCommon


class IntrastatProductCommon(IntrastatCommon):
    @classmethod
    def _init_products(cls):
        # Create category - don't init intrastat values, do it in tests
        vals = {
            "name": "Robots",
            "parent_id": cls.category_saleable.id,
        }
        cls.categ_robots = cls.category_obj.create(vals)

        vals = {
            "name": "C3PO",
            "type": "consu",
            "categ_id": cls.categ_robots.id,
            "origin_country_id": cls.env.ref("base.us").id,
            "weight": 300,
            # Computer - C3PO is one of them
            "hs_code_id": cls.hs_code_computer.id,
            "list_price": 42,
        }
        cls.product_c3po = cls.product_template_obj.create(vals)

    @classmethod
    def _init_company(cls):
        # Default transport for company is Road
        cls.demo_company.intrastat_transport_id = cls.transport_road

    @classmethod
    def _init_fiscal_position(cls):
        vals = {
            "name": "Intrastat Fiscal Position",
            "intrastat": "b2b",
            "vat_required": True,
        }
        cls.position = cls.position_obj.create(vals)

    @classmethod
    def _init_regions(cls):
        # Create Region
        cls._create_region()

        vals = {
            "code": "DE",
            "name": "Germany",
            "country_id": cls.env.ref("base.de").id,
            "description": "Germany",
        }
        cls._create_region(vals)

    @classmethod
    def _init_transaction(cls):
        vals = {
            "code": "9X",
            "company_id": cls.env.company.id,
            "description": "Test 9X",
        }
        cls._create_transaction(vals)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.region_obj = cls.env["intrastat.region"]
        cls.transaction_obj = cls.env["intrastat.transaction"]
        cls.transport_mode_obj = cls.env["intrastat.transport_mode"]
        cls.partner_obj = cls.env["res.partner"]
        cls.category_saleable = cls.env.ref("product.product_category_1")
        cls.category_obj = cls.env["product.category"]
        cls.product_template_obj = cls.env["product.template"]
        cls.declaration_obj = cls.env["intrastat.product.declaration"]
        cls.position_obj = cls.env["account.fiscal.position"]
        cls.hs_code_computer = cls.env.ref("product_harmonized_system.84715000")
        cls.report_obj = cls.env["ir.actions.report"]
        cls.xls_declaration = cls.env[
            "report.intrastat_product.product_declaration_xls"
        ]

        cls.transport_rail = cls.env.ref("intrastat_product.intrastat_transport_2")
        cls.transport_road = cls.env.ref("intrastat_product.intrastat_transport_3")

        cls._init_regions()
        cls._init_company()
        cls._init_fiscal_position()
        cls._init_products()
        cls._init_transaction()

    @classmethod
    def _create_xls(cls, declaration=False):
        """
            Prepare the Excel report to be tested

        :return: The Excel file
        :rtype: bytes
        """
        report = cls.env.ref(
            "intrastat_product.intrastat_product_xlsx_report"
        ).with_context(active_ids=cls.declaration.ids)
        report_name = report.report_name
        cls.report = cls.report_obj._get_report_from_name(report_name)
        datas = {
            "context": {
                "active_ids": [cls.declaration.id],
            }
        }
        data = {}
        encoded_data = "report/report_xlsx/" + report_name + "?" + url_encode(data)
        datas["data"] = encoded_data
        active_model = cls.declaration._name
        if not declaration:
            computation_lines = True
        else:
            computation_lines = False
        file_data = cls.xls_declaration.with_context(
            computation_lines=computation_lines, active_model=active_model
        ).create_xlsx_report(None, datas)
        return file_data

    def check_xls(self, xls):
        """
            Check that the xls content correspond to computation/declaration
            lines values

        :param xls: the Excel file content
        :type xls: bytes
        :param declaration: By default, check computation lines, either declaration ones
        :type declaration: bool, optional
        """
        book = xlrd.open_workbook(file_contents=xls)
        # Get the template used to build the Excel file lines
        template = self.xls_declaration._get_template(self.declaration)
        # Get the declaration lines or the computation ones
        to_test = [
            (
                book.sheet_by_index(0),
                self.declaration.computation_line_ids,
                self.declaration._xls_computation_line_fields(),
            ),
            (
                book.sheet_by_index(1),
                self.declaration.declaration_line_ids,
                self.declaration._xls_declaration_line_fields(),
            ),
        ]
        # Iterate on each row beginning on third one (two headers)
        for (sheet, lines, line_fields) in to_test:
            i = 0
            for rx in range(3, sheet.nrows):
                line = lines[i]
                row = sheet.row(rx)
                j = 0
                dict_compare = dict()
                for line_field in line_fields:
                    column_spec = template.get(line_field)
                    dict_compare.update(
                        {row[j].value: column_spec.get("line").get("value")}
                    )
                    j += 1
                for key, value in dict_compare.items():
                    value_eval = self.xls_declaration._eval(value, {"line": line})
                    self.assertEqual(key, value_eval)
                i += 1

    @classmethod
    def _create_region(cls, vals=None):
        values = {
            "code": "2",
            "country_id": cls.env.ref("base.be").id,
            "company_id": cls.env.company.id,
            "description": "Belgium Walloon Region",
            "name": "Walloon Region",
        }
        if vals is not None:
            values.update(vals)
        cls.region = cls.region_obj.create(values)

    @classmethod
    def _create_transaction(cls, vals=None):
        values = {
            "code": "11",
            "company_id": cls.env.company.id,
            "description": "Sale / Purchase",
        }
        if vals is not None:
            values.update(vals)
        cls.transaction = cls.transaction_obj.create(values)

    @classmethod
    def _create_transport_mode(cls, vals=None):
        values = {}
        if vals is not None:
            values.update(vals)
        cls.transport_mode = cls.transport_mode_obj.create(values)

    @classmethod
    def _create_declaration(cls, vals=None):
        values = {
            "company_id": cls.env.company.id,
            "declaration_type": "dispatches",
        }
        if vals is not None:
            values.update(vals)
        cls.declaration = cls.declaration_obj.create(values)
