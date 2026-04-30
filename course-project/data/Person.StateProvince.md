# Person.StateProvince

> State and province lookup table.

**Documentation:** AdventureWorks
**Schema:** Person
**Name:** StateProvince
**Module:** People

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | StateProvinceID | int | - | Identity | - | Primary key for StateProvince records. |
| - | 2 | - | StateProvinceCode | nchar(3) | - | - | - | ISO standard state or province code. |
| - | 3 | - | CountryRegionCode | nvarchar(3) | - | - | Person.CountryRegion | ISO standard country or region code. Foreign key to CountryRegion.CountryRegionCode. |
| - | 4 | - | IsOnlyStateProvinceFlag | bit | - | Default: 1 | - | 0 = StateProvinceCode exists. 1 = StateProvinceCode unavailable, using CountryRegionCode. |
| - | 5 | - | Name | nvarchar(50) | - | - | - | State or province description. |
| - | 6 | - | TerritoryID | int | - | - | Sales.SalesTerritory | ID of the territory in which the state or province is located. Foreign key to SalesTerritory.SalesTerritoryID. |
| - | 7 | - | rowguid | uniqueidentifier | - | Default: newid() | - | ROWGUIDCOL number uniquely identifying the record. Used to support a merge replication sample. |
| - | 8 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Person.StateProvince | - | Person.CountryRegion | Person.StateProvince.CountryRegionCode = Person.CountryRegion.CountryRegionCode | FK_StateProvince_CountryRegion_CountryRegionCode Foreign key constraint referencing CountryRegion.CountryRegionCode. |
| Person.StateProvince | - | Sales.SalesTerritory | Person.StateProvince.TerritoryID = Sales.SalesTerritory.TerritoryID | FK_StateProvince_SalesTerritory_TerritoryID Foreign key constraint referencing SalesTerritory.TerritoryID. |
| Person.Address | - | Person.StateProvince | Person.Address.StateProvinceID = Person.StateProvince.StateProvinceID | FK_Address_StateProvince_StateProvinceID Foreign key constraint referencing StateProvince.StateProvinceID. |
| Sales.SalesTaxRate | - | Person.StateProvince | Sales.SalesTaxRate.StateProvinceID = Person.StateProvince.StateProvinceID | FK_SalesTaxRate_StateProvince_StateProvinceID Foreign key constraint referencing StateProvince.StateProvinceID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_StateProvince_StateProvinceID | StateProvinceID | Primary key (clustered) constraint |
| - | AK_StateProvince_Name | Name | Unique nonclustered index. |
| - | AK_StateProvince_rowguid | rowguid | Unique nonclustered index. Used to support replication samples. |
| - | AK_StateProvince_StateProvinceCode_CountryRegionCode | StateProvinceCode, CountryRegionCode | Unique nonclustered index. |