# Copyright 2026 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from psycopg2 import IntegrityError

from odoo.tests import Form, TransactionCase
from odoo.tools import mute_logger


class TestHsCode(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.hs_code_model = cls.env["hs.code"]
        cls.hs_code = cls._create_hs_code("12345678")

    @classmethod
    def _create_hs_code(cls, local_code):
        """Create an H.S. code the way the user does it from its form view."""
        hs_code_form = Form(cls.hs_code_model)
        hs_code_form.local_code = local_code
        return hs_code_form.save()

    def test_local_code_uniq(self):
        with mute_logger("odoo.sql_db"), self.assertRaises(IntegrityError):
            self._create_hs_code("12345678")

    def test_local_code_uniq_spaces_ignored(self):
        """Spaces are stripped on save, so this is the same code as the existing
        one and must be rejected as well."""
        with mute_logger("odoo.sql_db"), self.assertRaises(IntegrityError):
            self._create_hs_code("1234 5678")

    def test_local_code_uniq_archived(self):
        """An archived code still reserves its local code."""
        self.hs_code.action_archive()
        with mute_logger("odoo.sql_db"), self.assertRaises(IntegrityError):
            self._create_hs_code("12345678")

    def test_local_code_uniq_write(self):
        """Renaming a code into an existing one is rejected too."""
        other_hs_code = self._create_hs_code("87654321")
        with mute_logger("odoo.sql_db"), self.assertRaises(IntegrityError):
            other_hs_code.local_code = "12345678"
            other_hs_code.flush_recordset()
