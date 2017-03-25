[![Runbot Status](https://runbot.odoo-community.org/runbot/badge/flat/227/8.0.svg)](https://runbot.odoo-community.org/runbot/repo/github-com-oca-intrastat-227)
[![Build Status](https://travis-ci.org/OCA/intrastat.svg?branch=8.0)](https://travis-ci.org/OCA/intrastat)
[![Coverage Status](https://coveralls.io/repos/OCA/intrastat/badge.svg?branch=8.0&service=github)](https://coveralls.io/github/OCA/intrastat?branch=8.0)
[![Code Climate](https://codeclimate.com/github/OCA/intrastat/badges/gpa.svg)](https://codeclimate.com/github/OCA/intrastat)

Intrastat Framework
===================

This repo contains a set of common modules for the Intrastat reporting and
should be used in combination with country-specific reporting modules
such as:

- *l10n_fr_intrastat_service*:
  the module for the *Déclaration Européenne des Services* (DES) for France
- *l10n_fr_intrastat_product*:
  the module for the *Déclaration d'Echange de Biens* (DEB) for France
- *l10n_be_intrastat_product*:
  the module for the Intrastat Declaration for Belgium.

[//]: # (addons)

Available addons
----------------
addon | version | summary
--- | --- | ---
[intrastat_base](intrastat_base/) | 8.0.1.3.0 | Base module for Intrastat reporting
[intrastat_product](intrastat_product/) | 8.0.1.4.1 | Base module for Intrastat Product
[product_harmonized_system](product_harmonized_system/) | 8.0.0.2.0 | Base module for Product Import/Export reports

[//]: # (end addons)

Translation Status
------------------
[![Transifex Status](https://www.transifex.com/projects/p/OCA-intrastat-8-0/chart/image_png)](https://www.transifex.com/projects/p/OCA-intrastat-8-0)

----

OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.
