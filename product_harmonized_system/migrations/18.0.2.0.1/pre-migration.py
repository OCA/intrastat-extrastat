# Copyright 2026 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging

from openupgradelib import openupgrade
from openupgradelib.openupgrade_merge_records import merge_records

_logger = logging.getLogger(__name__)


def _get_duplicated_codes(env):
    """Return the groups of H.S. codes sharing the same local code.

    Every group is a list of record ids sorted by the criteria electing the
    record to keep, which therefore comes first:

    1. The records owning an external ID, so the data of the module that
       declared them still resolves. Otherwise that module would recreate the
       record on its next update and reintroduce the duplicate.
    2. The active ones, as the archived records are the discarded leftovers.
    3. The oldest one, as it is the one the historical documents point to.
    """
    env.cr.execute(
        """
        WITH code AS (
            SELECT
                hc.id,
                hc.local_code,
                hc.active,
                EXISTS (
                    SELECT 1 FROM ir_model_data imd
                    WHERE imd.model = 'hs.code' AND imd.res_id = hc.id
                ) AS has_xmlid
            FROM hs_code hc
        )
        SELECT
            local_code,
            array_agg(id ORDER BY has_xmlid DESC, active DESC NULLS LAST, id)
        FROM code
        GROUP BY local_code
        HAVING count(id) > 1
        """
    )
    return env.cr.fetchall()


@openupgrade.migrate()
def migrate(env, version):
    """Merge the H.S. codes sharing the same local code.

    The `local_code_uniq` constraint introduced in this version is silently
    skipped with a warning when the table already holds duplicates, so they
    have to be gone before the module tables are updated.
    """
    for local_code, ids in _get_duplicated_codes(env):
        keep_id, drop_ids = ids[0], tuple(ids[1:])
        _logger.info(
            "H.S. codes %s merged into %s as they all use the local code %s",
            list(drop_ids),
            keep_id,
            local_code,
        )
        # Keep the external IDs of the discarded records resolving to the kept
        # one instead of leaving them dangling.
        openupgrade.logged_query(
            env.cr,
            """
            UPDATE ir_model_data SET res_id = %(keep_id)s
            WHERE model = 'hs.code' AND res_id IN %(drop_ids)s
            """,
            {"keep_id": keep_id, "drop_ids": drop_ids},
            skip_no_result=True,
        )
        # Recover the descriptions only filled in the discarded records, and
        # unarchive the kept one when any of them was still in use.
        openupgrade.logged_query(
            env.cr,
            """
            UPDATE hs_code hc SET
                description = COALESCE(hc.description, (
                    SELECT d.description FROM hs_code d
                    WHERE d.id IN %(drop_ids)s AND d.description IS NOT NULL
                    ORDER BY d.id LIMIT 1
                )),
                long_description = COALESCE(hc.long_description, (
                    SELECT d.long_description FROM hs_code d
                    WHERE d.id IN %(drop_ids)s AND d.long_description IS NOT NULL
                    ORDER BY d.id LIMIT 1
                )),
                active = COALESCE(hc.active, FALSE) OR EXISTS (
                    SELECT 1 FROM hs_code d
                    WHERE d.id IN %(drop_ids)s AND d.active
                )
            WHERE hc.id = %(keep_id)s
            """,
            {"keep_id": keep_id, "drop_ids": drop_ids},
        )
        # Redirect every record referencing the discarded codes and delete them
        merge_records(env, "hs.code", drop_ids, keep_id, method="sql")
