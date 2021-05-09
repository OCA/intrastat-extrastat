# Copyright 2021 ForgeFlow <http://www.forgeflow.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade


def fill_hs_code_company_id(env):
    # to avoid local_code_company_uniq constraint error
    openupgrade.logged_query(
        env.cr, """
        ALTER TABLE hs_code
        DROP CONSTRAINT IF EXISTS hs_code_local_code_company_uniq
        """)
    openupgrade.logged_query(
        env.cr, """
            UPDATE hs_code hc
            SET company_id = ru.company_id
            FROM res_users ru
            WHERE hc.create_uid = ru.id AND hc.company_id IS NULL"""
    )


@openupgrade.migrate()
def migrate(env, version):
    fill_hs_code_company_id(env)
