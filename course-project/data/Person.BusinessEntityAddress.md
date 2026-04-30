# Person.BusinessEntityAddress

> Cross-reference table mapping customers, vendors, and employees to their addresses.

**Documentation:** AdventureWorks
**Schema:** Person
**Name:** BusinessEntityAddress
**Module:** People

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | BusinessEntityID | int | - | - | Person.BusinessEntity | Primary key. Foreign key to BusinessEntity.BusinessEntityID. |
| - | 2 | - | AddressID | int | - | - | Person.Address | Primary key. Foreign key to Address.AddressID. |
| - | 3 | - | AddressTypeID | int | - | - | Person.AddressType | Primary key. Foreign key to AddressType.AddressTypeID. |
| - | 4 | - | rowguid | uniqueidentifier | - | Default: newid() | - | ROWGUIDCOL number uniquely identifying the record. Used to support a merge replication sample. |
| - | 5 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Person.BusinessEntityAddress | - | Person.Address | Person.BusinessEntityAddress.AddressID = Person.Address.AddressID | FK_BusinessEntityAddress_Address_AddressID Foreign key constraint referencing Address.AddressID. |
| Person.BusinessEntityAddress | - | Person.AddressType | Person.BusinessEntityAddress.AddressTypeID = Person.AddressType.AddressTypeID | FK_BusinessEntityAddress_AddressType_AddressTypeID Foreign key constraint referencing AddressType.AddressTypeID. |
| Person.BusinessEntityAddress | - | Person.BusinessEntity | Person.BusinessEntityAddress.BusinessEntityID = Person.BusinessEntity.BusinessEntityID | FK_BusinessEntityAddress_BusinessEntity_BusinessEntityID Foreign key constraint referencing BusinessEntity.BusinessEntityID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_BusinessEntityAddress_BusinessEntityID_AddressID_AddressTypeID | BusinessEntityID, AddressID, AddressTypeID | Primary key (clustered) constraint |
| - | AK_BusinessEntityAddress_rowguid | rowguid | Unique nonclustered index. Used to support replication samples. |