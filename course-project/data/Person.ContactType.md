# Person.ContactType

> Lookup table containing the types of business entity contacts.

**Documentation:** AdventureWorks
**Schema:** Person
**Name:** ContactType
**Module:** People

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | ContactTypeID | int | - | Identity | - | Primary key for ContactType records. |
| - | 2 | - | Name | nvarchar(50) | - | - | - | Contact type description. |
| - | 3 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Person.BusinessEntityContact | - | Person.ContactType | Person.BusinessEntityContact.ContactTypeID = Person.ContactType.ContactTypeID | FK_BusinessEntityContact_ContactType_ContactTypeID Foreign key constraint referencing ContactType.ContactTypeID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_ContactType_ContactTypeID | ContactTypeID | Primary key (clustered) constraint |
| - | AK_ContactType_Name | Name | Unique nonclustered index. |