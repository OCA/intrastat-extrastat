============
HS Code Link
============

Odoo added a field char field `hs_code` in the delivery module.
It results in a duplicate field from `product_harmonized_system` and it can be
seen twice in the `product.template` form view.

The goal of this module is to hide Odoo's field in the form and make it related
to the OCA's one if it is used elsewhere.

Installation
============

This module is set as auto_install if the following modules are installed:

* product_harmonized_system
* delivery

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

Contributors
------------

* Denis Leemann <denis.leemann@camptocamp.com>

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit https://odoo-community.org.
