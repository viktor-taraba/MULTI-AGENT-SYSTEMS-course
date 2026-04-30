# Person.BusinessEntityContact

> Cross-reference table mapping stores, vendors, and employees to people

**Documentation:** AdventureWorks
**Schema:** Person
**Name:** BusinessEntityContact
**Module:** People

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | BusinessEntityID | int | - | - | Person.BusinessEntity | Primary key. Foreign key to BusinessEntity.BusinessEntityID. |
| - | 2 | - | PersonID | int | - | - | Person.Person | Primary key. Foreign key to Person.BusinessEntityID. |
| - | 3 | - | ContactTypeID | int | - | - | Person.ContactType | Primary key. Foreign key to ContactType.ContactTypeID. |
| - | 4 | - | rowguid | uniqueidentifier | - | Default: newid() | - | ROWGUIDCOL number uniquely identifying the record. Used to support a merge replication sample. |
| - | 5 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Person.BusinessEntityContact | - | Person.BusinessEntity | Person.BusinessEntityContact.BusinessEntityID = Person.BusinessEntity.BusinessEntityID | FK_BusinessEntityContact_BusinessEntity_BusinessEntityID Foreign key constraint referencing BusinessEntity.BusinessEntityID. |
| Person.BusinessEntityContact | - | Person.ContactType | Person.BusinessEntityContact.ContactTypeID = Person.ContactType.ContactTypeID | FK_BusinessEntityContact_ContactType_ContactTypeID Foreign key constraint referencing ContactType.ContactTypeID. |
| Person.BusinessEntityContact | - | Person.Person | Person.BusinessEntityContact.PersonID = Person.Person.BusinessEntityID | FK_BusinessEntityContact_Person_PersonID Foreign key constraint referencing Person.BusinessEntityID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_BusinessEntityContact_BusinessEntityID_PersonID_ContactTypeID | BusinessEntityID, PersonID, ContactTypeID | Primary key (clustered) constraint |
| - | AK_BusinessEntityContact_rowguid | rowguid | Unique nonclustered index. Used to support replication samples. |