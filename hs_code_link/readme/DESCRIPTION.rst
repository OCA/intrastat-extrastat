Odoo added a field char field `hs_code` in the delivery module.
It results in a duplicate field from `product_harmonized_system` and it can be
seen twice in the `product.template` form view.

The goal of this module is to hide Odoo's field in the form and make it related
to the OCA's one if it is used elsewhere.
