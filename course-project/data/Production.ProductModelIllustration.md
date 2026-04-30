# Production.ProductModelIllustration

> Cross-reference table mapping product models and illustrations.

**Documentation:** AdventureWorks
**Schema:** Production
**Name:** ProductModelIllustration
**Module:** Products

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | ProductModelID | int | - | - | Production.ProductModel | Primary key. Foreign key to ProductModel.ProductModelID. |
| - | 2 | - | IllustrationID | int | - | - | Production.Illustration | Primary key. Foreign key to Illustration.IllustrationID. |
| - | 3 | - | ModifiedDate | datetime | - | Default: getdate() | Production.ProductModelProductDescriptionCulture | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Production.ProductModelIllustration | - | Production.Illustration | Production.ProductModelIllustration.IllustrationID = Production.Illustration.IllustrationID | FK_ProductModelIllustration_Illustration_IllustrationID Foreign key constraint referencing Illustration.IllustrationID. |
| Production.ProductModelIllustration | - | Production.ProductModel | Production.ProductModelIllustration.ProductModelID = Production.ProductModel.ProductModelID | FK_ProductModelIllustration_ProductModel_ProductModelID Foreign key constraint referencing ProductModel.ProductModelID. |
| Production.ProductModelIllustration | - | Production.ProductModelProductDescriptionCulture | Production.ProductModelIllustration.ModifiedDate = Production.ProductModelProductDescriptionCulture.ProductDescriptionID | fk_ProductModelProductDescriptionCulture_ProductModelIllustration |
| Production.ProductCategory | - | Production.ProductModelIllustration | Production.ProductCategory.Name = Production.ProductModelIllustration.ProductModelID Production.ProductCategory.Name = Production.ProductModelIllustration.IllustrationID | fk_ProductModelIllustration_ProductCategory |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_ProductModelIllustration_ProductModelID_IllustrationID | ProductModelID, IllustrationID | Primary key (clustered) constraint |