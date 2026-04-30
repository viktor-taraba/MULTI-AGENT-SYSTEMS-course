# Production.ProductModelProductDescriptionCulture

> Cross-reference table mapping product descriptions and the language the description is written in.

**Documentation:** AdventureWorks
**Schema:** Production
**Name:** ProductModelProductDescriptionCulture
**Module:** Products

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | ProductModelID | int | - | - | Production.ProductModel | Primary key. Foreign key to ProductModel.ProductModelID. |
| - | 2 | - | ProductDescriptionID | int | - | - | Production.ProductDescription | Primary key. Foreign key to ProductDescription.ProductDescriptionID. |
| - | 3 | - | CultureID | nchar(6) | - | - | Production.Culture | Culture identification number. Foreign key to Culture.CultureID. |
| - | 4 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Production.ProductModelProductDescriptionCulture | - | Production.Culture | Production.ProductModelProductDescriptionCulture.CultureID = Production.Culture.CultureID | FK_ProductModelProductDescriptionCulture_Culture_CultureID Foreign key constraint referencing Culture.CultureID. |
| Production.ProductModelProductDescriptionCulture | - | Production.ProductDescription | Production.ProductModelProductDescriptionCulture.ProductDescriptionID = Production.ProductDescription.ProductDescriptionID | FK_ProductModelProductDescriptionCulture_ProductDescription_ProductDescriptionID Foreign key constraint referencing ProductDescription.ProductDescriptionID. |
| Production.ProductModelProductDescriptionCulture | - | Production.ProductModel | Production.ProductModelProductDescriptionCulture.ProductModelID = Production.ProductModel.ProductModelID | FK_ProductModelProductDescriptionCulture_ProductModel_ProductModelID Foreign key constraint referencing ProductModel.ProductModelID. |
| Production.ProductModelIllustration | - | Production.ProductModelProductDescriptionCulture | Production.ProductModelIllustration.ModifiedDate = Production.ProductModelProductDescriptionCulture.ProductDescriptionID | fk_ProductModelProductDescriptionCulture_ProductModelIllustration |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_ProductModelProductDescriptionCulture_ProductModelID_ProductDescriptionID_CultureID | ProductModelID, ProductDescriptionID, CultureID | Primary key (clustered) constraint |