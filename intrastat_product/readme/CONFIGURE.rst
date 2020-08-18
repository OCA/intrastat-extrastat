By default the intrastat declaration is generated based upon the product record master data.
Hence unexpected results may occur in case this master data is not accurate,
e.g. wrong or missing weight, country of origin, ...

|

This can be corrected by changing the appropriate fields when analysing the intrastat declaration
but this can be challenging in case of large transaction volumes and especially in the specific use
case where the product weight cannot be encoded correctly on the product records (e.g. products with variable weight).

|

It is possible to allow encoding the intrastat transaction details on the purchase/sale invoice
via the "intrastat_product.group_invoice_intrastat_transaction_detail" usability group.
