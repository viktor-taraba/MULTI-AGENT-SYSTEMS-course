# Production.TransactionHistory

> Record of each purchase order, sales order, or work order transaction year to date.

**Documentation:** AdventureWorks
**Schema:** Production
**Name:** TransactionHistory
**Module:** Manufacturing

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | TransactionID | int | - | Identity | - | Primary key for TransactionHistory records. |
| - | 2 | - | ProductID | int | - | - | Production.Product | Product identification number. Foreign key to Product.ProductID. |
| - | 3 | - | ReferenceOrderID | int | - | - | - | Purchase order, sales order, or work order identification number. |
| - | 4 | - | ReferenceOrderLineID | int | - | Default: 0 | - | Line number associated with the purchase order, sales order, or work order. |
| - | 5 | - | TransactionDate | datetime | - | Default: getdate() | - | Date and time of the transaction. |
| - | 6 | - | TransactionType | nchar(1) | - | - | - | W = WorkOrder, S = SalesOrder, P = PurchaseOrder |
| - | 7 | - | Quantity | int | - | - | - | Product quantity. |
| - | 8 | - | ActualCost | money | - | - | - | Product cost. |
| - | 9 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Production.TransactionHistory | - | Production.Product | Production.TransactionHistory.ProductID = Production.Product.ProductID | FK_TransactionHistory_Product_ProductID Foreign key constraint referencing Product.ProductID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_TransactionHistory_TransactionID | TransactionID | Primary key (clustered) constraint |