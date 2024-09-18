#   Copyright (c) 2024 Groupe Voltaire
#   @author Emilie SOUTIRAS  <emilie.soutiras@groupevoltaire.com>
#   License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Product Harmonized System Codes per countries",
    "version": "16.0.1.1.0",
    "category": "Reporting",
    "license": "AGPL-3",
    "summary": "Module for to custom H.S. Codes par country",
    "author": "Emilie SOUTIRAS, Groupe Voltaire, Odoo Community Association (OCA)",
    "maintainers": ["emiliesoutiras"],
    "website": "https://github.com/OCA/intrastat-extrastat",
    "depends": ["delivery", "intrastat_product"],
    "data": [
        "views/hs_code.xml",
        "report/deliveryslip_report.xml",
    ],
    "installable": True,
}
