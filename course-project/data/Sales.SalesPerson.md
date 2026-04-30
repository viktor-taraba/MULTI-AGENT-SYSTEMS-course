# Sales.SalesPerson

> Sales representative current information.

**Documentation:** AdventureWorks
**Schema:** Sales
**Name:** SalesPerson
**Module:** Sales

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | BusinessEntityID | int | - | - | HumanResources.Employee | Primary key for SalesPerson records. Foreign key to Employee.BusinessEntityID |
| - | 2 | - | TerritoryID | int | - | - | Sales.SalesTerritory | Territory currently assigned to. Foreign key to SalesTerritory.SalesTerritoryID. |
| - | 3 | - | SalesQuota | money | - | - | - | Projected yearly sales. |
| - | 4 | - | Bonus | money | - | Default: 0.00 | - | Bonus due if quota is met. |
| - | 5 | - | CommissionPct | smallmoney | - | Default: 0.00 | - | Commision percent received per sale. |
| - | 6 | - | SalesYTD | money | - | Default: 0.00 | - | Sales total year to date. |
| - | 7 | - | SalesLastYear | money | - | Default: 0.00 | - | Sales total of previous year. |
| - | 8 | - | rowguid | uniqueidentifier | - | Default: newid() | - | ROWGUIDCOL number uniquely identifying the record. Used to support a merge replication sample. |
| - | 9 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Sales.SalesPerson | - | HumanResources.Employee | Sales.SalesPerson.BusinessEntityID = HumanResources.Employee.BusinessEntityID | FK_SalesPerson_Employee_BusinessEntityID Foreign key constraint referencing Employee.EmployeeID. |
| Sales.SalesPerson | - | Sales.SalesTerritory | Sales.SalesPerson.TerritoryID = Sales.SalesTerritory.TerritoryID | FK_SalesPerson_SalesTerritory_TerritoryID Foreign key constraint referencing SalesTerritory.TerritoryID. |
| Sales.SalesOrderHeader | - | Sales.SalesPerson | Sales.SalesOrderHeader.SalesPersonID = Sales.SalesPerson.BusinessEntityID | FK_SalesOrderHeader_SalesPerson_SalesPersonID Foreign key constraint referencing SalesPerson.SalesPersonID. |
| Sales.SalesPersonQuotaHistory | - | Sales.SalesPerson | Sales.SalesPersonQuotaHistory.BusinessEntityID = Sales.SalesPerson.BusinessEntityID | FK_SalesPersonQuotaHistory_SalesPerson_BusinessEntityID Foreign key constraint referencing SalesPerson.SalesPersonID. |
| Sales.SalesTerritoryHistory | - | Sales.SalesPerson | Sales.SalesTerritoryHistory.BusinessEntityID = Sales.SalesPerson.BusinessEntityID | FK_SalesTerritoryHistory_SalesPerson_BusinessEntityID Foreign key constraint referencing SalesPerson.SalesPersonID. |
| Sales.Store | - | Sales.SalesPerson | Sales.Store.SalesPersonID = Sales.SalesPerson.BusinessEntityID | FK_Store_SalesPerson_SalesPersonID Foreign key constraint referencing SalesPerson.SalesPersonID |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_SalesPerson_BusinessEntityID | BusinessEntityID | Primary key (clustered) constraint |
| - | AK_SalesPerson_rowguid | rowguid | Unique nonclustered index. Used to support replication samples. |