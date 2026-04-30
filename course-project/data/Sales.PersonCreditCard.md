# Sales.PersonCreditCard

> Cross-reference table mapping people to their credit card information in the CreditCard table.

**Documentation:** AdventureWorks
**Schema:** Sales
**Name:** PersonCreditCard
**Module:** Sales

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | BusinessEntityID | int | - | - | Person.Person | Business entity identification number. Foreign key to Person.BusinessEntityID. |
| - | 2 | - | CreditCardID | int | - | - | Sales.CreditCard | Credit card identification number. Foreign key to CreditCard.CreditCardID. |
| - | 3 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Sales.PersonCreditCard | - | Sales.CreditCard | Sales.PersonCreditCard.CreditCardID = Sales.CreditCard.CreditCardID | FK_PersonCreditCard_CreditCard_CreditCardID Foreign key constraint referencing CreditCard.CreditCardID. |
| Sales.PersonCreditCard | - | Person.Person | Sales.PersonCreditCard.BusinessEntityID = Person.Person.BusinessEntityID | FK_PersonCreditCard_Person_BusinessEntityID Foreign key constraint referencing Person.BusinessEntityID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_PersonCreditCard_BusinessEntityID_CreditCardID | BusinessEntityID, CreditCardID | Primary key (clustered) constraint |