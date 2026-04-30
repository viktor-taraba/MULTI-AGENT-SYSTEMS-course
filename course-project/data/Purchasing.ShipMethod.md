# Purchasing.ShipMethod

> Shipping company lookup table.

**Documentation:** AdventureWorks
**Schema:** Purchasing
**Name:** ShipMethod
**Module:** Purchasing

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | ShipMethodID | int | - | Identity | - | Primary key for ShipMethod records. |
| - | 2 | - | Name | nvarchar(50) | - | - | - | Shipping company name. |
| - | 3 | - | ShipBase | money | - | Default: 0.00 | - | Minimum shipping charge. |
| - | 4 | - | ShipRate | money | - | Default: 0.00 | - | Shipping charge per pound. |
| - | 5 | - | rowguid | uniqueidentifier | - | Default: newid() | - | ROWGUIDCOL number uniquely identifying the record. Used to support a merge replication sample. |
| - | 6 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Purchasing.PurchaseOrderHeader | - | Purchasing.ShipMethod | Purchasing.PurchaseOrderHeader.ShipMethodID = Purchasing.ShipMethod.ShipMethodID | FK_PurchaseOrderHeader_ShipMethod_ShipMethodID Foreign key constraint referencing ShipMethod.ShipMethodID. |
| Sales.SalesOrderHeader | - | Purchasing.ShipMethod | Sales.SalesOrderHeader.ShipMethodID = Purchasing.ShipMethod.ShipMethodID | FK_SalesOrderHeader_ShipMethod_ShipMethodID Foreign key constraint referencing ShipMethod.ShipMethodID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_ShipMethod_ShipMethodID | ShipMethodID | Primary key (clustered) constraint |
| - | AK_ShipMethod_Name | Name | Unique nonclustered index. |
| - | AK_ShipMethod_rowguid | rowguid | Unique nonclustered index. Used to support replication samples. |