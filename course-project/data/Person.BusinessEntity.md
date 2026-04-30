# Person.BusinessEntity

> Source of the ID that connects vendors, customers, and employees with address and contact information.

**Documentation:** AdventureWorks
**Schema:** Person
**Name:** BusinessEntity
**Module:** People

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | BusinessEntityID | int | - | Identity | - | Primary key for all customers, vendors, and employees. |
| - | 2 | - | rowguid | uniqueidentifier | - | Default: newid() | - | ROWGUIDCOL number uniquely identifying the record. Used to support a merge replication sample. |
| - | 3 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Person.BusinessEntityAddress | - | Person.BusinessEntity | Person.BusinessEntityAddress.BusinessEntityID = Person.BusinessEntity.BusinessEntityID | FK_BusinessEntityAddress_BusinessEntity_BusinessEntityID Foreign key constraint referencing BusinessEntity.BusinessEntityID. |
| Person.BusinessEntityContact | - | Person.BusinessEntity | Person.BusinessEntityContact.BusinessEntityID = Person.BusinessEntity.BusinessEntityID | FK_BusinessEntityContact_BusinessEntity_BusinessEntityID Foreign key constraint referencing BusinessEntity.BusinessEntityID. |
| Person.Person | - | Person.BusinessEntity | Person.Person.BusinessEntityID = Person.BusinessEntity.BusinessEntityID | FK_Person_BusinessEntity_BusinessEntityID Foreign key constraint referencing BusinessEntity.BusinessEntityID. |
| Sales.Store | - | Person.BusinessEntity | Sales.Store.BusinessEntityID = Person.BusinessEntity.BusinessEntityID | FK_Store_BusinessEntity_BusinessEntityID Foreign key constraint referencing BusinessEntity.BusinessEntityID |
| Purchasing.Vendor | - | Person.BusinessEntity | Purchasing.Vendor.BusinessEntityID = Person.BusinessEntity.BusinessEntityID | FK_Vendor_BusinessEntity_BusinessEntityID Foreign key constraint referencing BusinessEntity.BusinessEntityID |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_BusinessEntity_BusinessEntityID | BusinessEntityID | Primary key (clustered) constraint |
| - | AK_BusinessEntity_rowguid | rowguid | Unique nonclustered index. Used to support replication samples. |