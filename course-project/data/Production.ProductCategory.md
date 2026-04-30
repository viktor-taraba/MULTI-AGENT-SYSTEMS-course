# Production.ProductCategory

> High-level product categorization.

**Documentation:** AdventureWorks
**Schema:** Production
**Name:** ProductCategory
**Module:** Products

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | ProductCategoryID | int | - | Identity | - | Primary key for ProductCategory records. |
| - | 2 | - | Name | nvarchar(50) | - | - | Production.ProductModelIllustration | Category description. |
| - | 3 | - | rowguid | uniqueidentifier | - | Default: newid() | - | ROWGUIDCOL number uniquely identifying the record. Used to support a merge replication sample. |
| - | 4 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Production.ProductCategory | - | Production.ProductModelIllustration | Production.ProductCategory.Name = Production.ProductModelIllustration.ProductModelID Production.ProductCategory.Name = Production.ProductModelIllustration.IllustrationID | fk_ProductModelIllustration_ProductCategory |
| Production.ProductSubcategory | - | Production.ProductCategory | Production.ProductSubcategory.ProductCategoryID = Production.ProductCategory.ProductCategoryID | FK_ProductSubcategory_ProductCategory_ProductCategoryID Foreign key constraint referencing ProductCategory.ProductCategoryID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_ProductCategory_ProductCategoryID | ProductCategoryID | Primary key (clustered) constraint |
| - | AK_ProductCategory_Name | Name | Unique nonclustered index. |
| - | AK_ProductCategory_rowguid | rowguid | Unique nonclustered index. Used to support replication samples. |