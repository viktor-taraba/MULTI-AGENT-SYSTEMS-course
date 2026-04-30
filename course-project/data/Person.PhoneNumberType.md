# Person.PhoneNumberType

> Type of phone number of a person.

**Documentation:** AdventureWorks
**Schema:** Person
**Name:** PhoneNumberType
**Module:** People

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | PhoneNumberTypeID | int | - | Identity | - | Primary key for telephone number type records. |
| - | 2 | - | Name | nvarchar(50) | - | - | - | Name of the telephone number type |
| - | 3 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Person.PersonPhone | - | Person.PhoneNumberType | Person.PersonPhone.PhoneNumberTypeID = Person.PhoneNumberType.PhoneNumberTypeID | FK_PersonPhone_PhoneNumberType_PhoneNumberTypeID Foreign key constraint referencing PhoneNumberType.PhoneNumberTypeID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_PhoneNumberType_PhoneNumberTypeID | PhoneNumberTypeID | Primary key (clustered) constraint |