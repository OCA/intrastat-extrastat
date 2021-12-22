# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from psycopg2 import IntegrityError

from odoo.exceptions import UserError, ValidationError
from odoo.tests.common import SavepointCase
from odoo.tools import mute_logger

from .common import IntrastatProductCommon


class TestIntrastatProduct(IntrastatProductCommon):
    """Tests for this module"""

    # Test duplicates
    @mute_logger("odoo.sql_db")
    def test_region(self):
        with self.assertRaises(IntegrityError):
            self._create_region()

    @mute_logger("odoo.sql_db")
    def test_transaction(self):
        self._create_transaction()
        with self.assertRaises(IntegrityError):
            self._create_transaction()

    @mute_logger("odoo.sql_db")
    def test_transport_mode(self):
        vals = {"code": 1, "name": "Sea"}
        with self.assertRaises(IntegrityError):
            self._create_transport_mode(vals)

    def test_copy(self):
        """
        When copying declaration, the new one has an incremented revision
        value.
        """
        vals = {"declaration_type": "dispatches"}
        self._create_declaration(vals)
        decl_copy = self.declaration.copy()
        self.assertEqual(self.declaration.revision + 1, decl_copy.revision)

    def test_declaration_no_country(self):
        self.demo_company.country_id = False
        with self.assertRaises(ValidationError):
            self._create_declaration()
            self.declaration.flush()

    def test_declaration_no_vat(self):
        self.demo_company.partner_id.vat = False
        with self.assertRaises(UserError):
            self._create_declaration()
            self.declaration.flush()
            self.declaration._check_generate_xml()

    def test_declaration_state(self):
        self._create_declaration()
        self.declaration.unlink()

        self._create_declaration()
        self.declaration.state = "done"
        with self.assertRaises(UserError):
            self.declaration.unlink()


class TestIntrastatProductCase(TestIntrastatProduct, SavepointCase):
    """ Test Intrastat Product """
