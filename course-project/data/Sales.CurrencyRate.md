# Sales.CurrencyRate

> Currency exchange rates.

**Documentation:** AdventureWorks
**Schema:** Sales
**Name:** CurrencyRate
**Module:** Sales

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | CurrencyRateID | int | - | Identity | - | Primary key for CurrencyRate records. |
| - | 2 | - | CurrencyRateDate | datetime | - | - | - | Date and time the exchange rate was obtained. |
| - | 3 | - | FromCurrencyCode | nchar(3) | - | - | Sales.Currency | Exchange rate was converted from this currency code. |
| - | 4 | - | ToCurrencyCode | nchar(3) | - | - | Sales.Currency | Exchange rate was converted to this currency code. |
| - | 5 | - | AverageRate | money | - | - | - | Average exchange rate for the day. |
| - | 6 | - | EndOfDayRate | money | - | - | - | Final exchange rate for the day. |
| - | 7 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Sales.CurrencyRate | - | Sales.Currency | Sales.CurrencyRate.FromCurrencyCode = Sales.Currency.CurrencyCode | FK_CurrencyRate_Currency_FromCurrencyCode Foreign key constraint referencing Currency.FromCurrencyCode. |
| Sales.CurrencyRate | - | Sales.Currency | Sales.CurrencyRate.ToCurrencyCode = Sales.Currency.CurrencyCode | FK_CurrencyRate_Currency_ToCurrencyCode Foreign key constraint referencing Currency.FromCurrencyCode. |
| Sales.SalesOrderHeader | - | Sales.CurrencyRate | Sales.SalesOrderHeader.CurrencyRateID = Sales.CurrencyRate.CurrencyRateID | FK_SalesOrderHeader_CurrencyRate_CurrencyRateID Foreign key constraint referencing CurrencyRate.CurrencyRateID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_CurrencyRate_CurrencyRateID | CurrencyRateID | Primary key (clustered) constraint |
| - | AK_CurrencyRate_CurrencyRateDate_FromCurrencyCode_ToCurrencyCode | CurrencyRateDate, FromCurrencyCode, ToCurrencyCode | Unique nonclustered index. |