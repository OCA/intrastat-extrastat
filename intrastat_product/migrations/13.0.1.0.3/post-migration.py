# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade  # pylint: disable=W7936

_months = [
    (1, "01"),
    (2, "02"),
    (3, "03"),
    (4, "04"),
    (5, "05"),
    (6, "06"),
    (7, "07"),
    (8, "08"),
    (9, "09"),
    (10, "10"),
    (11, "11"),
    (12, "12"),
]


def map_intrastat_product_declaration_month(env):
    openupgrade.map_values(
        env.cr,
        openupgrade.get_legacy_name("month"),
        "month",
        _months,
        table="intrastat_product_declaration",
    )


def update_invoice_relation_fields(env):
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE account_move am
        SET (intrastat_transaction_id, intrastat_transport_id,
            src_dest_country_id, intrastat_country, src_dest_region_id
            ) = (ai.intrastat_transaction_id,
            ai.intrastat_transport_id, ai.src_dest_country_id,
            ai.intrastat_country, ai.src_dest_region_id)
        FROM account_invoice ai
        WHERE am.old_invoice_id = ai.id""",
    )
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE intrastat_product_computation_line ipcl
        SET invoice_line_id = aml.id
        FROM account_invoice_line ail
        JOIN account_move_line aml ON aml.old_invoice_line_id = ail.id
        WHERE ipcl.%(old_line_id)s = ail.id"""
        % {"old_line_id": openupgrade.get_legacy_name("invoice_line_id")},
    )


@openupgrade.migrate()
def migrate(env, version):
    map_intrastat_product_declaration_month(env)
    update_invoice_relation_fields(env)
    openupgrade.load_data(
        env.cr, "intrastat_product", "migrations/13.0.1.0.3/noupdate_changes.xml"
    )
