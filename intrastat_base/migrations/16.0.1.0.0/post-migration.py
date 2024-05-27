# Copyright 2024 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    # Set proper values for new selection field
    old_column = openupgrade.get_legacy_name("intrastat")
    openupgrade.logged_query(
        env.cr,
        f"""
        UPDATE account_fiscal_position
        SET intrastat = CASE
        WHEN NOT {old_column} THEN 'no'
        ELSE 'b2b' END
        """,
    )
    # Propagate proper values to the related field
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE account_move am
        SET intrastat_fiscal_position = afp.intrastat
        FROM account_fiscal_position afp
        WHERE afp.id = am.fiscal_position_id
        """,
    )
