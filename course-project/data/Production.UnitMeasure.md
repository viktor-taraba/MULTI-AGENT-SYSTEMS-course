# Production.UnitMeasure

> Unit of measure lookup table.

**Documentation:** AdventureWorks
**Schema:** Production
**Name:** UnitMeasure
**Module:** Products

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | UnitMeasureCode | nchar(3) | - | - | - | Primary key. |
| - | 2 | - | Name | nvarchar(50) | - | - | - | Unit of measure description. |
| - | 3 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Production.BillOfMaterials | - | Production.UnitMeasure | Production.BillOfMaterials.UnitMeasureCode = Production.UnitMeasure.UnitMeasureCode | FK_BillOfMaterials_UnitMeasure_UnitMeasureCode Foreign key constraint referencing UnitMeasure.UnitMeasureCode. |
| Production.Product | - | Production.UnitMeasure | Production.Product.SizeUnitMeasureCode = Production.UnitMeasure.UnitMeasureCode | FK_Product_UnitMeasure_SizeUnitMeasureCode Foreign key constraint referencing UnitMeasure.UnitMeasureCode. |
| Production.Product | - | Production.UnitMeasure | Production.Product.WeightUnitMeasureCode = Production.UnitMeasure.UnitMeasureCode | FK_Product_UnitMeasure_WeightUnitMeasureCode Foreign key constraint referencing UnitMeasure.UnitMeasureCode. |
| Purchasing.ProductVendor | - | Production.UnitMeasure | Purchasing.ProductVendor.UnitMeasureCode = Production.UnitMeasure.UnitMeasureCode | FK_ProductVendor_UnitMeasure_UnitMeasureCode Foreign key constraint referencing UnitMeasure.UnitMeasureCode. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_UnitMeasure_UnitMeasureCode | UnitMeasureCode | Primary key (clustered) constraint |
| - | AK_UnitMeasure_Name | Name | Unique nonclustered index. |