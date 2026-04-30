# Sales.SalesOrderHeaderSalesReason

> Cross-reference table mapping sales orders to sales reason codes.

**Documentation:** AdventureWorks
**Schema:** Sales
**Name:** SalesOrderHeaderSalesReason
**Module:** Sales

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | SalesOrderID | int | - | - | Sales.SalesOrderHeader | Primary key. Foreign key to SalesOrderHeader.SalesOrderID. |
| - | 2 | - | SalesReasonID | int | - | - | Sales.SalesReason | Primary key. Foreign key to SalesReason.SalesReasonID. |
| - | 3 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Sales.SalesOrderHeaderSalesReason | - | Sales.SalesOrderHeader | Sales.SalesOrderHeaderSalesReason.SalesOrderID = Sales.SalesOrderHeader.SalesOrderID | FK_SalesOrderHeaderSalesReason_SalesOrderHeader_SalesOrderID Foreign key constraint referencing SalesOrderHeader.SalesOrderID. |
| Sales.SalesOrderHeaderSalesReason | - | Sales.SalesReason | Sales.SalesOrderHeaderSalesReason.SalesReasonID = Sales.SalesReason.SalesReasonID | FK_SalesOrderHeaderSalesReason_SalesReason_SalesReasonID Foreign key constraint referencing SalesReason.SalesReasonID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_SalesOrderHeaderSalesReason_SalesOrderID_SalesReasonID | SalesOrderID, SalesReasonID | Primary key (clustered) constraint |