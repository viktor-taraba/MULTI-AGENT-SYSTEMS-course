# Sales.SalesTerritoryHistory

> Sales representative transfers to other sales territories.

**Documentation:** AdventureWorks
**Schema:** Sales
**Name:** SalesTerritoryHistory
**Module:** Sales

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | BusinessEntityID | int | - | - | Sales.SalesPerson | Primary key. The sales rep. Foreign key to SalesPerson.BusinessEntityID. |
| - | 2 | - | TerritoryID | int | - | - | Sales.SalesTerritory | Primary key. Territory identification number. Foreign key to SalesTerritory.SalesTerritoryID. |
| - | 3 | - | StartDate | datetime | - | - | - | Primary key. Date the sales representive started work in the territory. |
| - | 4 | - | EndDate | datetime | - | - | - | Date the sales representative left work in the territory. |
| - | 5 | - | rowguid | uniqueidentifier | - | Default: newid() | - | ROWGUIDCOL number uniquely identifying the record. Used to support a merge replication sample. |
| - | 6 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Sales.SalesTerritoryHistory | - | Sales.SalesPerson | Sales.SalesTerritoryHistory.BusinessEntityID = Sales.SalesPerson.BusinessEntityID | FK_SalesTerritoryHistory_SalesPerson_BusinessEntityID Foreign key constraint referencing SalesPerson.SalesPersonID. |
| Sales.SalesTerritoryHistory | - | Sales.SalesTerritory | Sales.SalesTerritoryHistory.TerritoryID = Sales.SalesTerritory.TerritoryID | FK_SalesTerritoryHistory_SalesTerritory_TerritoryID Foreign key constraint referencing SalesTerritory.TerritoryID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_SalesTerritoryHistory_BusinessEntityID_StartDate_TerritoryID | BusinessEntityID, TerritoryID, StartDate | Primary key (clustered) constraint |
| - | AK_SalesTerritoryHistory_rowguid | rowguid | Unique nonclustered index. Used to support replication samples. |