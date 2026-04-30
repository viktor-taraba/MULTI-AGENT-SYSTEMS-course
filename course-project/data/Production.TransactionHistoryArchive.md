# Production.TransactionHistoryArchive

> Transactions for previous years.

**Documentation:** AdventureWorks
**Schema:** Production
**Name:** TransactionHistoryArchive
**Module:** Manufacturing

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | TransactionID | int | - | - | - | Primary key for TransactionHistoryArchive records. |
| - | 2 | - | ProductID | int | - | - | Production.Product | Product identification number. Foreign key to Product.ProductID. |
| - | 3 | - | ReferenceOrderID | int | - | - | - | Purchase order, sales order, or work order identification number. |
| - | 4 | - | ReferenceOrderLineID | int | - | Default: 0 | - | Line number associated with the purchase order, sales order, or work order. |
| - | 5 | - | TransactionDate | datetime | - | Default: getdate() | - | Date and time of the transaction. |
| - | 6 | - | TransactionType | nchar(1) | - | - | - | W = Work Order, S = Sales Order, P = Purchase Order |
| - | 7 | - | Quantity | int | - | - | - | Product quantity. |
| - | 8 | - | ActualCost | money | - | - | - | Product cost. |
| - | 9 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Production.TransactionHistoryArchive | - | Production.Product | Production.TransactionHistoryArchive.ProductID = Production.Product.ProductID | User-defined relation |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_TransactionHistoryArchive_TransactionID | TransactionID | Primary key (clustered) constraint |