# Person.Password

> One way hashed authentication information

**Documentation:** AdventureWorks
**Schema:** Person
**Name:** Password
**Module:** People

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | BusinessEntityID | int | - | - | Person.Person | - |
| - | 2 | - | PasswordHash | varchar(128) | - | - | - | Password for the e-mail account. |
| - | 3 | - | PasswordSalt | varchar(10) | - | - | - | Random value concatenated with the password string before the password is hashed. |
| - | 4 | - | rowguid | uniqueidentifier | - | Default: newid() | - | ROWGUIDCOL number uniquely identifying the record. Used to support a merge replication sample. |
| - | 5 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Person.Password | - | Person.Person | Person.Password.BusinessEntityID = Person.Person.BusinessEntityID | FK_Password_Person_BusinessEntityID Foreign key constraint referencing Person.BusinessEntityID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_Password_BusinessEntityID | BusinessEntityID | Primary key (clustered) constraint |