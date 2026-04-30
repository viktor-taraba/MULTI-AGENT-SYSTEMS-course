# Person.EmailAddress

> Where to send a person email.

**Documentation:** AdventureWorks
**Schema:** Person
**Name:** EmailAddress
**Module:** People

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | BusinessEntityID | int | - | - | Person.Person | Primary key. Person associated with this email address. Foreign key to Person.BusinessEntityID |
| - | 2 | - | EmailAddressID | int | - | Identity | - | Primary key. ID of this email address. |
| - | 3 | - | EmailAddress | nvarchar(50) | - | - | - | E-mail address for the person. |
| - | 4 | - | rowguid | uniqueidentifier | - | Default: newid() | - | ROWGUIDCOL number uniquely identifying the record. Used to support a merge replication sample. |
| - | 5 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Person.EmailAddress | - | Person.Person | Person.EmailAddress.BusinessEntityID = Person.Person.BusinessEntityID | FK_EmailAddress_Person_BusinessEntityID Foreign key constraint referencing Person.BusinessEntityID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_EmailAddress_BusinessEntityID_EmailAddressID | BusinessEntityID, EmailAddressID | Primary key (clustered) constraint |