# Person.AddressType

> Types of addresses stored in the Address table.

**Documentation:** AdventureWorks
**Schema:** Person
**Name:** AddressType
**Module:** People

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | AddressTypeID | int | - | Identity | - | Primary key for AddressType records. |
| - | 2 | - | Name | nvarchar(50) | - | - | - | Address type description. For example, Billing, Home, or Shipping. |
| - | 3 | - | rowguid | uniqueidentifier | - | Default: newid() | - | ROWGUIDCOL number uniquely identifying the record. Used to support a merge replication sample. |
| - | 4 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Person.BusinessEntityAddress | - | Person.AddressType | Person.BusinessEntityAddress.AddressTypeID = Person.AddressType.AddressTypeID | FK_BusinessEntityAddress_AddressType_AddressTypeID Foreign key constraint referencing AddressType.AddressTypeID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_AddressType_AddressTypeID | AddressTypeID | Primary key (clustered) constraint |
| - | AK_AddressType_Name | Name | Unique nonclustered index. |
| - | AK_AddressType_rowguid | rowguid | Unique nonclustered index. Used to support replication samples. |