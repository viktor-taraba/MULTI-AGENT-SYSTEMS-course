# Sales.SalesTerritory

> Sales territory lookup table.

**Documentation:** AdventureWorks
**Schema:** Sales
**Name:** SalesTerritory
**Module:** Sales

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | TerritoryID | int | - | Identity | - | Primary key for SalesTerritory records. |
| - | 2 | - | Name | nvarchar(50) | - | - | - | Sales territory description |
| - | 3 | - | CountryRegionCode | nvarchar(3) | - | - | Person.CountryRegion | ISO standard country or region code. Foreign key to CountryRegion.CountryRegionCode. |
| - | 4 | - | Group | nvarchar(50) | - | - | - | Geographic area to which the sales territory belong. |
| - | 5 | - | SalesYTD | money | - | Default: 0.00 | - | Sales in the territory year to date. |
| - | 6 | - | SalesLastYear | money | - | Default: 0.00 | - | Sales in the territory the previous year. |
| - | 7 | - | CostYTD | money | - | Default: 0.00 | - | Business costs in the territory year to date. |
| - | 8 | - | CostLastYear | money | - | Default: 0.00 | - | Business costs in the territory the previous year. |
| - | 9 | - | rowguid | uniqueidentifier | - | Default: newid() | - | ROWGUIDCOL number uniquely identifying the record. Used to support a merge replication sample. |
| - | 10 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Sales.SalesTerritory | - | Person.CountryRegion | Sales.SalesTerritory.CountryRegionCode = Person.CountryRegion.CountryRegionCode | FK_SalesTerritory_CountryRegion_CountryRegionCode Foreign key constraint referencing CountryRegion.CountryRegionCode. |
| Sales.Customer | - | Sales.SalesTerritory | Sales.Customer.TerritoryID = Sales.SalesTerritory.TerritoryID | FK_Customer_SalesTerritory_TerritoryID Foreign key constraint referencing SalesTerritory.TerritoryID. |
| Sales.SalesOrderHeader | - | Sales.SalesTerritory | Sales.SalesOrderHeader.TerritoryID = Sales.SalesTerritory.TerritoryID | FK_SalesOrderHeader_SalesTerritory_TerritoryID Foreign key constraint referencing SalesTerritory.TerritoryID. |
| Sales.SalesPerson | - | Sales.SalesTerritory | Sales.SalesPerson.TerritoryID = Sales.SalesTerritory.TerritoryID | FK_SalesPerson_SalesTerritory_TerritoryID Foreign key constraint referencing SalesTerritory.TerritoryID. |
| Sales.SalesTerritoryHistory | - | Sales.SalesTerritory | Sales.SalesTerritoryHistory.TerritoryID = Sales.SalesTerritory.TerritoryID | FK_SalesTerritoryHistory_SalesTerritory_TerritoryID Foreign key constraint referencing SalesTerritory.TerritoryID. |
| Person.StateProvince | - | Sales.SalesTerritory | Person.StateProvince.TerritoryID = Sales.SalesTerritory.TerritoryID | FK_StateProvince_SalesTerritory_TerritoryID Foreign key constraint referencing SalesTerritory.TerritoryID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_SalesTerritory_TerritoryID | TerritoryID | Primary key (clustered) constraint |
| - | AK_SalesTerritory_Name | Name | Unique nonclustered index. |
| - | AK_SalesTerritory_rowguid | rowguid | Unique nonclustered index. Used to support replication samples. |