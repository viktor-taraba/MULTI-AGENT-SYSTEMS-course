# Sales.CountryRegionCurrency

> Cross-reference table mapping ISO currency codes to a country or region.

**Documentation:** AdventureWorks
**Schema:** Sales
**Name:** CountryRegionCurrency
**Module:** Sales

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | CountryRegionCode | nvarchar(3) | - | - | Person.CountryRegion | ISO code for countries and regions. Foreign key to CountryRegion.CountryRegionCode. |
| - | 2 | - | CurrencyCode | nchar(3) | - | - | Sales.Currency | ISO standard currency code. Foreign key to Currency.CurrencyCode. |
| - | 3 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Sales.CountryRegionCurrency | - | Person.CountryRegion | Sales.CountryRegionCurrency.CountryRegionCode = Person.CountryRegion.CountryRegionCode | FK_CountryRegionCurrency_CountryRegion_CountryRegionCode Foreign key constraint referencing CountryRegion.CountryRegionCode. |
| Sales.CountryRegionCurrency | - | Sales.Currency | Sales.CountryRegionCurrency.CurrencyCode = Sales.Currency.CurrencyCode | FK_CountryRegionCurrency_Currency_CurrencyCode Foreign key constraint referencing Currency.CurrencyCode. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_CountryRegionCurrency_CountryRegionCode_CurrencyCode | CountryRegionCode, CurrencyCode | Primary key (clustered) constraint |