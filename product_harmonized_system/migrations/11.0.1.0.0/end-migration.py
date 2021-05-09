# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# Copyright 2021 ForgeFlow <http://www.forgeflow.com>

from openupgradelib import openupgrade  # pylint: disable=W7936
from openupgradelib import openupgrade_merge_records  # pylint: disable=W7936


def merge_duplicated_hs_codes(env):
    # if exist duplicates, remove them
    openupgrade.logged_query(
        env.cr, """
        WITH duplicated AS (
            SELECT count(*), local_code, company_id
            FROM hs_code
            GROUP BY local_code, company_id
            HAVING count(*) > 1
        )
        SELECT hc.id, hc.local_code, hc.company_id
        FROM hs_code hc
        JOIN duplicated ON (hc.local_code = duplicated.local_code
            AND hc.company_id = duplicated.company_id)
        ORDER BY hc.active DESC NULLS LAST, hc.id ASC
        """
    )
    companies = {}
    for hs_code_id, local_code, company_id in env.cr.fetchall():
        companies.setdefault(company_id, {}).setdefault(
            local_code, []).append(hs_code_id)
    for company_id in companies:
        for local_code in companies[company_id]:
            openupgrade_merge_records.merge_records(
                env, "hs.code", companies[company_id][local_code],
                companies[company_id][local_code][0],
                method='sql', delete=True,
                exclude_columns=None, model_table="hs_code")


@openupgrade.migrate()
def migrate(env, version):
    merge_duplicated_hs_codes(env)
