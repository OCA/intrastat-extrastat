# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# Copyright 2021 ForgeFlow <http://www.forgeflow.com>

from openupgradelib import openupgrade  # pylint: disable=W7936


def update_intrastat_product_declaration_year(env):
    openupgrade.logged_query(
        env.cr, """
        UPDATE intrastat_product_declaration
        SET year = {integer_year} || ''
        """.format(integer_year=openupgrade.get_legacy_name("year"))
    )


@openupgrade.migrate()
def migrate(env, version):
    update_intrastat_product_declaration_year(env)
