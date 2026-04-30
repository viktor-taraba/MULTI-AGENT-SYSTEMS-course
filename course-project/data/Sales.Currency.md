# Sales.Currency

> Lookup table containing standard ISO currencies.

**Documentation:** AdventureWorks
**Schema:** Sales
**Name:** Currency
**Module:** Sales

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | CurrencyCode | nchar(3) | - | - | - | The ISO code for the Currency. |
| - | 2 | - | Name | nvarchar(50) | - | - | - | Currency name. |
| - | 3 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Sales.CountryRegionCurrency | - | Sales.Currency | Sales.CountryRegionCurrency.CurrencyCode = Sales.Currency.CurrencyCode | FK_CountryRegionCurrency_Currency_CurrencyCode Foreign key constraint referencing Currency.CurrencyCode. |
| Sales.CurrencyRate | - | Sales.Currency | Sales.CurrencyRate.FromCurrencyCode = Sales.Currency.CurrencyCode | FK_CurrencyRate_Currency_FromCurrencyCode Foreign key constraint referencing Currency.FromCurrencyCode. |
| Sales.CurrencyRate | - | Sales.Currency | Sales.CurrencyRate.ToCurrencyCode = Sales.Currency.CurrencyCode | FK_CurrencyRate_Currency_ToCurrencyCode Foreign key constraint referencing Currency.FromCurrencyCode. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_Currency_CurrencyCode | CurrencyCode | Primary key (clustered) constraint |
| - | AK_Currency_Name | Name | Unique nonclustered index. |