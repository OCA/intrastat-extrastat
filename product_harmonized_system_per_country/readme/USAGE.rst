This module depends on the *delivery* module and the *intrastat_product* module, which depends on the *product_harmonized_systems* module.

This module adds the 'applicable country' field to the HS Code model, and enables HS Codes to be linked together as parent/child, so that the code corresponding to the destination country can be dynamically found from a single HS Code.