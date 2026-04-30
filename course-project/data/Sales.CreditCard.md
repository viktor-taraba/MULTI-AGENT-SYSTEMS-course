# Sales.CreditCard

> Customer credit card information.

**Documentation:** AdventureWorks
**Schema:** Sales
**Name:** CreditCard
**Module:** Sales

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | CreditCardID | int | - | Identity | - | Primary key for CreditCard records. |
| - | 2 | - | CardType | nvarchar(50) | - | - | - | Credit card name. |
| - | 3 | - | CardNumber | nvarchar(25) | - | - | - | Credit card number. |
| - | 4 | - | ExpMonth | tinyint | - | - | - | Credit card expiration month. |
| - | 5 | - | ExpYear | smallint | - | - | - | Credit card expiration year. |
| - | 6 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Sales.PersonCreditCard | - | Sales.CreditCard | Sales.PersonCreditCard.CreditCardID = Sales.CreditCard.CreditCardID | FK_PersonCreditCard_CreditCard_CreditCardID Foreign key constraint referencing CreditCard.CreditCardID. |
| Sales.SalesOrderHeader | - | Sales.CreditCard | Sales.SalesOrderHeader.CreditCardID = Sales.CreditCard.CreditCardID | FK_SalesOrderHeader_CreditCard_CreditCardID Foreign key constraint referencing CreditCard.CreditCardID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_CreditCard_CreditCardID | CreditCardID | Primary key (clustered) constraint |
| - | AK_CreditCard_CardNumber | CardNumber | Unique nonclustered index. |