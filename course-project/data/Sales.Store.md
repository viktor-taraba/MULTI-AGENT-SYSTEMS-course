# Sales.Store

> Customers (resellers) of Adventure Works products.

**Documentation:** AdventureWorks
**Schema:** Sales
**Name:** Store
**Module:** Sales

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | BusinessEntityID | int | - | - | Person.BusinessEntity | Primary key. Foreign key to Customer.BusinessEntityID. |
| - | 2 | - | Name | nvarchar(50) | - | - | - | Name of the store. |
| - | 3 | - | SalesPersonID | int | - | - | Sales.SalesPerson | ID of the sales person assigned to the customer. Foreign key to SalesPerson.BusinessEntityID. |
| - | 4 | - | Demographics | xml | - | - | - | Demographic informationg about the store such as the number of employees, annual sales and store type. |
| - | 5 | - | rowguid | uniqueidentifier | - | Default: newid() | - | ROWGUIDCOL number uniquely identifying the record. Used to support a merge replication sample. |
| - | 6 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Sales.Store | - | Person.BusinessEntity | Sales.Store.BusinessEntityID = Person.BusinessEntity.BusinessEntityID | FK_Store_BusinessEntity_BusinessEntityID Foreign key constraint referencing BusinessEntity.BusinessEntityID |
| Sales.Store | - | Sales.SalesPerson | Sales.Store.SalesPersonID = Sales.SalesPerson.BusinessEntityID | FK_Store_SalesPerson_SalesPersonID Foreign key constraint referencing SalesPerson.SalesPersonID |
| Sales.Customer | - | Sales.Store | Sales.Customer.StoreID = Sales.Store.BusinessEntityID | FK_Customer_Store_StoreID Foreign key constraint referencing Store.BusinessEntityID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_Store_BusinessEntityID | BusinessEntityID | Primary key (clustered) constraint |
| - | AK_Store_rowguid | rowguid | Unique nonclustered index. Used to support replication samples. |