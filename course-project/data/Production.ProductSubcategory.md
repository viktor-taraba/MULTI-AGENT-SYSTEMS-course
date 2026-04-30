# Production.ProductSubcategory

> Product subcategories. See ProductCategory table.

**Documentation:** AdventureWorks
**Schema:** Production
**Name:** ProductSubcategory
**Module:** Products

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | ProductSubcategoryID | int | - | Identity | - | Primary key for ProductSubcategory records. |
| - | 2 | - | ProductCategoryID | int | - | - | Production.ProductCategory | Product category identification number. Foreign key to ProductCategory.ProductCategoryID. |
| - | 3 | - | Name | nvarchar(50) | - | - | - | Subcategory description. |
| - | 4 | - | rowguid | uniqueidentifier | - | Default: newid() | - | ROWGUIDCOL number uniquely identifying the record. Used to support a merge replication sample. |
| - | 5 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Production.ProductSubcategory | - | Production.ProductCategory | Production.ProductSubcategory.ProductCategoryID = Production.ProductCategory.ProductCategoryID | FK_ProductSubcategory_ProductCategory_ProductCategoryID Foreign key constraint referencing ProductCategory.ProductCategoryID. |
| Production.Product | - | Production.ProductSubcategory | Production.Product.ProductSubcategoryID = Production.ProductSubcategory.ProductSubcategoryID | FK_Product_ProductSubcategory_ProductSubcategoryID Foreign key constraint referencing ProductSubcategory.ProductSubcategoryID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_ProductSubcategory_ProductSubcategoryID | ProductSubcategoryID | Primary key (clustered) constraint |
| - | AK_ProductSubcategory_Name | Name | Unique nonclustered index. |
| - | AK_ProductSubcategory_rowguid | rowguid | Unique nonclustered index. Used to support replication samples. |