# Production.ProductModel

> Product model classification.

**Documentation:** AdventureWorks
**Schema:** Production
**Name:** ProductModel
**Module:** Products

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | ProductModelID | int | - | Identity | - | Primary key for ProductModel records. |
| - | 2 | - | Name | nvarchar(50) | - | - | - | Product model description. |
| - | 3 | - | CatalogDescription | xml | - | - | - | Detailed product catalog information in xml format. |
| - | 4 | - | Instructions | xml | - | - | - | Manufacturing instructions in xml format. |
| - | 5 | - | rowguid | uniqueidentifier | - | Default: newid() | - | ROWGUIDCOL number uniquely identifying the record. Used to support a merge replication sample. |
| - | 6 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Production.Product | - | Production.ProductModel | Production.Product.ProductModelID = Production.ProductModel.ProductModelID | FK_Product_ProductModel_ProductModelID Foreign key constraint referencing ProductModel.ProductModelID. |
| Production.ProductModelIllustration | - | Production.ProductModel | Production.ProductModelIllustration.ProductModelID = Production.ProductModel.ProductModelID | FK_ProductModelIllustration_ProductModel_ProductModelID Foreign key constraint referencing ProductModel.ProductModelID. |
| Production.ProductModelProductDescriptionCulture | - | Production.ProductModel | Production.ProductModelProductDescriptionCulture.ProductModelID = Production.ProductModel.ProductModelID | FK_ProductModelProductDescriptionCulture_ProductModel_ProductModelID Foreign key constraint referencing ProductModel.ProductModelID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_ProductModel_ProductModelID | ProductModelID | Primary key (clustered) constraint |
| - | AK_ProductModel_Name | Name | Unique nonclustered index. |
| - | AK_ProductModel_rowguid | rowguid | Unique nonclustered index. Used to support replication samples. |