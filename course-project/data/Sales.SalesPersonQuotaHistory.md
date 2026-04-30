# Sales.SalesPersonQuotaHistory

> Sales performance tracking.

**Documentation:** AdventureWorks
**Schema:** Sales
**Name:** SalesPersonQuotaHistory
**Module:** Sales

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | BusinessEntityID | int | - | - | Sales.SalesPerson | Sales person identification number. Foreign key to SalesPerson.BusinessEntityID. |
| - | 2 | - | QuotaDate | datetime | - | - | - | Sales quota date. |
| - | 3 | - | SalesQuota | money | - | - | - | Sales quota amount. |
| - | 4 | - | rowguid | uniqueidentifier | - | Default: newid() | - | ROWGUIDCOL number uniquely identifying the record. Used to support a merge replication sample. |
| - | 5 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Sales.SalesPersonQuotaHistory | - | Sales.SalesPerson | Sales.SalesPersonQuotaHistory.BusinessEntityID = Sales.SalesPerson.BusinessEntityID | FK_SalesPersonQuotaHistory_SalesPerson_BusinessEntityID Foreign key constraint referencing SalesPerson.SalesPersonID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_SalesPersonQuotaHistory_BusinessEntityID_QuotaDate | BusinessEntityID, QuotaDate | Primary key (clustered) constraint |
| - | AK_SalesPersonQuotaHistory_rowguid | rowguid | Unique nonclustered index. Used to support replication samples. |