# Copyright 2022 Stefan Rijnhart <stefan@opener.amsterdam>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging


def pre_init_hook(cr):
    """Prepopulate stored computed fields for faster installation"""
    logger = logging.getLogger(__name__)
    logger.info("Prepopulating stored computed fields")
    cr.execute(
        """
        alter table account_move
        add column if not exists src_dest_country_id integer;
        """
    )
    cr.execute(
        """
        with countries as (
            select am.id as move_id,
            coalesce(
                rps.country_id,
                rp.country_id,
                rpc.country_id
            ) as country_id
            from account_move am
            left join res_partner rps on rps.id = am.partner_shipping_id
            join res_partner rp on rp.id = am.partner_id
            join res_company rc on rc.id = am.company_id
            join res_partner rpc on rpc.id = rc.partner_id
        )
        update account_move am
        set src_dest_country_id = countries.country_id
        from countries where am.id = countries.move_id;
        """
    )
