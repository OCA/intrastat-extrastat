# Copyright 2021 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    if not version:
        return

    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        pc_field_id = env.ref(
            "product_harmonized_system.field_product_category__hs_code_id"
        ).id
        cr.execute(
            """
            UPDATE product_category pc
            SET hs_code_id=SUBSTRING(ip.value_reference, 9, 99)::int
            FROM ir_property ip
            WHERE ip.res_id like 'product.category,%%' AND
            SUBSTRING(ip.res_id, 18, 99)::int=pc.id AND
            ip.name='hs_code_id' AND
            ip.value_reference IS NOT null AND
            ip.fields_id=%s
            """,
            (pc_field_id,),
        )
        pt_field_id = env.ref(
            "product_harmonized_system.field_product_template__hs_code_id"
        ).id
        cr.execute(
            """
            UPDATE product_template pt
            SET hs_code_id=SUBSTRING(ip.value_reference, 9, 99)::int
            FROM ir_property ip
            WHERE ip.res_id like 'product.template,%%' AND
            SUBSTRING(ip.res_id, 18, 99)::int=pt.id AND
            ip.name='hs_code_id' AND
            ip.value_reference IS NOT null AND
            ip.fields_id=%s
            """,
            (pt_field_id,),
        )
