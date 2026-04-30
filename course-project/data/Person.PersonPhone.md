# Person.PersonPhone

> Telephone number and type of a person.

**Documentation:** AdventureWorks
**Schema:** Person
**Name:** PersonPhone
**Module:** People

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | BusinessEntityID | int | - | - | Person.Person | Business entity identification number. Foreign key to Person.BusinessEntityID. |
| - | 2 | - | PhoneNumber | nvarchar(25) | - | - | - | Telephone number identification number. |
| - | 3 | - | PhoneNumberTypeID | int | - | - | Person.PhoneNumberType | Kind of phone number. Foreign key to PhoneNumberType.PhoneNumberTypeID. |
| - | 4 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Person.PersonPhone | - | Person.Person | Person.PersonPhone.BusinessEntityID = Person.Person.BusinessEntityID | FK_PersonPhone_Person_BusinessEntityID Foreign key constraint referencing Person.BusinessEntityID. |
| Person.PersonPhone | - | Person.PhoneNumberType | Person.PersonPhone.PhoneNumberTypeID = Person.PhoneNumberType.PhoneNumberTypeID | FK_PersonPhone_PhoneNumberType_PhoneNumberTypeID Foreign key constraint referencing PhoneNumberType.PhoneNumberTypeID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_PersonPhone_BusinessEntityID_PhoneNumber_PhoneNumberTypeID | BusinessEntityID, PhoneNumber, PhoneNumberTypeID | Primary key (clustered) constraint |