This addon allows you to define an "Incoterm" and an "Intrastat Transport Mode" at the
"Shipping Methods" of sales. When these values are established, they will be the ones
that prevail in the sales orders, if they are not defined, the default values that were
established in "Settings" will apply.

The mode of transport and incoterm are assigned to the sales order when it goes from
"Quotation" to "Order". Additionally, the values will be dragged to the invoices created
from that sales order.

It is recommended to set TRUE the "Show incoterms in orders and invoices" value at
"Settings / Sales".

Incoterm selection priority:

When assigning the Incoterm to a sales order, the following priority is applied:

1. First, the Incoterm set on the partner is used.
2. If not defined, the Incoterm from the shipping method is used.
3. If still not defined, the general settings Incoterm is used.
4. If none of the above are set, the Incoterm field remains empty.
