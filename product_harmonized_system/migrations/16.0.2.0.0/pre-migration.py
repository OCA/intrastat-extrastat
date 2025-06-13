from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_columns(env.cr, {"hs_code": [("company_id", None)]})
    rule = env.ref("product_harmonized_system.hs_code_company_rule")
    if rule:
        rule.unlink()
