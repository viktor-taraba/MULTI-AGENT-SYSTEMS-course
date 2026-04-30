# Sales.Customer

> Current customer information. Also see the Person and Store tables.

**Documentation:** AdventureWorks
**Schema:** Sales
**Name:** Customer
**Module:** Sales

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | CustomerID | int | - | Identity | - | Primary key. |
| - | 2 | - | PersonID | int | - | - | Person.Person | Foreign key to Person.BusinessEntityID |
| - | 3 | - | StoreID | int | - | - | Sales.Store | Foreign key to Store.BusinessEntityID |
| - | 4 | - | TerritoryID | int | - | - | Sales.SalesTerritory | ID of the territory in which the customer is located. Foreign key to SalesTerritory.SalesTerritoryID. |
| - | 5 | - | AccountNumber | varchar(10) | - | Computed: isnull('AW'+[ufnLeadingZeros]([CustomerID]),'') | - | Unique number identifying the customer assigned by the accounting system. |
| - | 6 | - | rowguid | uniqueidentifier | - | Default: newid() | - | ROWGUIDCOL number uniquely identifying the record. Used to support a merge replication sample. |
| - | 7 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Sales.Customer | - | Person.Person | Sales.Customer.PersonID = Person.Person.BusinessEntityID | FK_Customer_Person_PersonID Foreign key constraint referencing Person.BusinessEntityID. |
| Sales.Customer | - | Sales.SalesTerritory | Sales.Customer.TerritoryID = Sales.SalesTerritory.TerritoryID | FK_Customer_SalesTerritory_TerritoryID Foreign key constraint referencing SalesTerritory.TerritoryID. |
| Sales.Customer | - | Sales.Store | Sales.Customer.StoreID = Sales.Store.BusinessEntityID | FK_Customer_Store_StoreID Foreign key constraint referencing Store.BusinessEntityID. |
| Sales.SalesOrderHeader | - | Sales.Customer | Sales.SalesOrderHeader.CustomerID = Sales.Customer.CustomerID | FK_SalesOrderHeader_Customer_CustomerID Foreign key constraint referencing Customer.CustomerID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_Customer_CustomerID | CustomerID | Primary key (clustered) constraint |
| - | AK_Customer_AccountNumber | AccountNumber | Unique nonclustered index. |
| - | AK_Customer_rowguid | rowguid | Unique nonclustered index. Used to support replication samples. |