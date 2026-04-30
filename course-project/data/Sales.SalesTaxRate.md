# Sales.SalesTaxRate

> Tax rate lookup table.

**Documentation:** AdventureWorks
**Schema:** Sales
**Name:** SalesTaxRate
**Module:** Sales

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | SalesTaxRateID | int | - | Identity | - | Primary key for SalesTaxRate records. |
| - | 2 | - | StateProvinceID | int | - | - | Person.StateProvince | State, province, or country/region the sales tax applies to. |
| - | 3 | - | TaxType | tinyint | - | - | - | 1 = Tax applied to retail transactions, 2 = Tax applied to wholesale transactions, 3 = Tax applied to all sales (retail and wholesale) transactions. |
| - | 4 | - | TaxRate | smallmoney | - | Default: 0.00 | - | Tax rate amount. |
| - | 5 | - | Name | nvarchar(50) | - | - | - | Tax rate description. |
| - | 6 | - | rowguid | uniqueidentifier | - | Default: newid() | - | ROWGUIDCOL number uniquely identifying the record. Used to support a merge replication sample. |
| - | 7 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Sales.SalesTaxRate | - | Person.StateProvince | Sales.SalesTaxRate.StateProvinceID = Person.StateProvince.StateProvinceID | FK_SalesTaxRate_StateProvince_StateProvinceID Foreign key constraint referencing StateProvince.StateProvinceID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_SalesTaxRate_SalesTaxRateID | SalesTaxRateID | Primary key (clustered) constraint |
| - | AK_SalesTaxRate_rowguid | rowguid | Unique nonclustered index. Used to support replication samples. |
| - | AK_SalesTaxRate_StateProvinceID_TaxType | StateProvinceID, TaxType | Unique nonclustered index. |