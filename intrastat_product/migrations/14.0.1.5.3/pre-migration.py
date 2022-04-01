# Copyright 2022 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


def migrate(cr, version):
    if not version:
        return

    cr.execute("DELETE FROM ir_model_fields WHERE model = 'intrastat.common'")
    cr.execute("DELETE FROM ir_model WHERE model = 'intrastat.common'")
