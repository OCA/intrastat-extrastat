The OCA module *product_harmonized_system* adds a many2one field
*hs_code_id* on product templates that points to an *H.S. Code* object.
But the *delivery* module from the official addons adds a char field
*hs_code* on product templates, which has the same purpose, but we can't
use it because we need structured data for H.S. codes. This module hides
the *hs_code* field added by the *delivery* module, to avoid confusion.

Since Odoo v16, the *delivery* module also adds a many2one field
*country_of_origin*, which is similar to the many2one field
*origin_country_id* of the OCA module *product_harmonized_system*. This
module also hides the *country_of_origin* field added by the *delivery*
module.
