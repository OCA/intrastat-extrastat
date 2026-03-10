import io
from unittest.mock import patch

from odoo.exceptions import ValidationError
from odoo.fields import Command
from odoo.tools import mute_logger

from odoo.addons.account.models.chart_template import AccountChartTemplate

from .common import IntrastatCommon


def _get_chart_template_mapping(self, get_all=False):
    return {
        "test": {
            "name": "test",
            "country_id": self.env.ref("base.be").id,
            "country_code": None,
            "module": "account",
            "parent": None,
        }
    }


def test_get_data(self, template_code):
    """The template_data and res.company keys are required for proper operation."""
    return {
        "template_data": {},
        "res.company": {
            self.env.company.id: {},
        },
        "account.fiscal.position": {
            "test_fiscal_position_template": {
                "name": "Fiscal Position",
            }
        },
    }


CSV_DATA = {
    "test_fiscal_position_template": (
        '"id","name"\n"test_fiscal_position_template","Fiscal Position"\n'
    ),
}


class TestIntrastatBase(IntrastatCommon):
    """Tests for this module"""

    def test_company(self):
        # add 'Demo user' to intrastat_remind_user_ids
        self.demo_company.write(
            {"intrastat_remind_user_ids": [Command.set([self.demo_user.id])]}
        )
        # then check if intrastat_email_list contains the email of the user
        self.assertEqual(self.demo_company.intrastat_email_list, self.demo_user.email)

    def test_no_email(self):
        self.demo_user.email = False
        with self.assertRaises(ValidationError):
            self.demo_company.write(
                {"intrastat_remind_user_ids": [Command.set([self.demo_user.id])]}
            )

    def test_accessory(self):
        with self.assertRaises(ValidationError):
            self.shipping_cost.type = "consu"
            self.shipping_cost.is_accessory_cost = True

    def test_fiscal_position(self):
        with self.assertRaises(ValidationError):
            self.env["account.fiscal.position"].create(
                {
                    "name": "TestB2B",
                    "vat_required": False,
                    "intrastat": "b2b",
                }
            )
        with self.assertRaises(ValidationError):
            self.env["account.fiscal.position"].create(
                {
                    "name": "TestB2C",
                    "vat_required": True,
                    "intrastat": "b2c",
                }
            )

    @patch.object(
        AccountChartTemplate, "_get_chart_template_mapping", _get_chart_template_mapping
    )
    @mute_logger("odoo.models.unlink")
    def test_chart_template_fiscal_position(self):
        """Similar to what test_parsed_csv_submodel_being_updated does in account
        test_chart_template to check if the chart template has a tax position and the
        data defined in it is not "correct", the correct "default" value will be
        returned.
        We cannot use generic_coa because it does not have tax position data.
        """
        with patch.object(
            AccountChartTemplate,
            "_get_chart_template_data",
            side_effect=test_get_data,
            autospec=True,
        ):
            self.chart_template_obj._load(
                template_code="test", company=self.demo_company, install_demo=False
            )
        with patch(
            "odoo.addons.account.models.chart_template.file_open",
            side_effect=lambda *args: io.StringIO(
                CSV_DATA["test_fiscal_position_template"]
            ),
        ):
            data_fp = self.chart_template_obj._get_account_fiscal_position("test")
        self.assertIn("test_fiscal_position_template", data_fp)
        self.assertEqual(data_fp["test_fiscal_position_template"]["intrastat"], "no")
