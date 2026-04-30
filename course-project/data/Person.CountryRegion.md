# Person.CountryRegion

> Lookup table containing the ISO standard codes for countries and regions.

**Documentation:** AdventureWorks
**Schema:** Person
**Name:** CountryRegion
**Module:** People

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | CountryRegionCode | nvarchar(3) | - | - | - | ISO standard code for countries and regions. |
| - | 2 | - | Name | nvarchar(50) | - | - | - | Country or region name. |
| - | 3 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Sales.CountryRegionCurrency | - | Person.CountryRegion | Sales.CountryRegionCurrency.CountryRegionCode = Person.CountryRegion.CountryRegionCode | FK_CountryRegionCurrency_CountryRegion_CountryRegionCode Foreign key constraint referencing CountryRegion.CountryRegionCode. |
| Sales.SalesTerritory | - | Person.CountryRegion | Sales.SalesTerritory.CountryRegionCode = Person.CountryRegion.CountryRegionCode | FK_SalesTerritory_CountryRegion_CountryRegionCode Foreign key constraint referencing CountryRegion.CountryRegionCode. |
| Person.StateProvince | - | Person.CountryRegion | Person.StateProvince.CountryRegionCode = Person.CountryRegion.CountryRegionCode | FK_StateProvince_CountryRegion_CountryRegionCode Foreign key constraint referencing CountryRegion.CountryRegionCode. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_CountryRegion_CountryRegionCode | CountryRegionCode | Primary key (clustered) constraint |
| - | AK_CountryRegion_Name | Name | Unique nonclustered index. |