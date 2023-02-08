# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests.common import TransactionCase

from .common import IntrastatProductCommon


class TestIntrastatCompany(IntrastatProductCommon):
    """Tests for this module"""

    def test_company_values(self):
        # Exempt for arrivals and dispatches => exempt
        self.demo_company.update(
            {
                "intrastat_arrivals": "exempt",
                "intrastat_dispatches": "exempt",
            }
        )
        self.assertEqual("exempt", self.demo_company.intrastat)

        # Extended for arrivals or dispatches => extended
        self.demo_company.update(
            {
                "intrastat_arrivals": "extended",
            }
        )
        self.assertEqual("extended", self.demo_company.intrastat)

        # standard for arrivals or dispatches => standard
        self.demo_company.update(
            {
                "intrastat_arrivals": "exempt",
                "intrastat_dispatches": "standard",
            }
        )
        self.assertEqual("standard", self.demo_company.intrastat)


class TestIntrastatProductCase(TestIntrastatCompany, TransactionCase):
    """Test Intrastat Product"""
