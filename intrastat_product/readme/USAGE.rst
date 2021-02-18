This module is used in combination with the country-specific
localization module(s).

**Coding guidelines for localization module:**

We recommend to start by copying an existing module, e.g. l10n_be_intrastat_product
and adapt the code for the specific needs of your country.

* Declaration Object

  Create a new class as follows:

  .. code-block:: python

     class L10nCcIntrastatProductDeclaration(models.Model):
         _name = 'l10n.cc.intrastat.product.declaration'
         _description = "Intrastat Product Declaration for YourCountry"
         _inherit = ['intrastat.product.declaration', 'mail.thread']

  whereby cc = your country code

* Computation & Declaration Lines

  Create also new objects inheriting from the Computation and Declaration Line Objects
  so that you can add methods or customise the methods from the base modules (make a PR when
  the customization or new method is required for multiple countries).

  Adapt also the parent_id fields of the newly created objects
  (cf. l10n_be_intrastat_product as example).

* XML Files: Menu, Action, Views

  Cf. l10n_be_istrastat_product as example, replace "be" by your Country Code.

**Other functionality added by this module:**

* Compute the Intrastat Lines in an invoice.
  For this, your user needs to be in the "Technical / Invoice Intrastat Transaction Details" group.
  Go to the "Intrastat transaction details" tab and press **Compute**
