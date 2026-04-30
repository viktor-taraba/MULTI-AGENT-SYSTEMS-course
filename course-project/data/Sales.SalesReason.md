# Sales.SalesReason

> Lookup table of customer purchase reasons.

**Documentation:** AdventureWorks
**Schema:** Sales
**Name:** SalesReason
**Module:** Sales

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | SalesReasonID | int | - | Identity | - | Primary key for SalesReason records. |
| - | 2 | - | Name | nvarchar(50) | - | - | - | Sales reason description. |
| - | 3 | - | ReasonType | nvarchar(50) | - | - | - | Category the sales reason belongs to. |
| - | 4 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Sales.SalesOrderHeaderSalesReason | - | Sales.SalesReason | Sales.SalesOrderHeaderSalesReason.SalesReasonID = Sales.SalesReason.SalesReasonID | FK_SalesOrderHeaderSalesReason_SalesReason_SalesReasonID Foreign key constraint referencing SalesReason.SalesReasonID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_SalesReason_SalesReasonID | SalesReasonID | Primary key (clustered) constraint |