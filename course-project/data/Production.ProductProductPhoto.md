# Production.ProductProductPhoto

> Cross-reference table mapping products and product photos.

**Documentation:** AdventureWorks
**Schema:** Production
**Name:** ProductProductPhoto
**Module:** Products

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | ProductID | int | - | - | Production.Product | Product identification number. Foreign key to Product.ProductID. |
| - | 2 | - | ProductPhotoID | int | - | - | Production.ProductPhoto | Product photo identification number. Foreign key to ProductPhoto.ProductPhotoID. |
| - | 3 | - | Primary | bit | - | Default: 0 | - | 0 = Photo is not the principal image. 1 = Photo is the principal image. |
| - | 4 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Production.ProductProductPhoto | - | Production.Product | Production.ProductProductPhoto.ProductID = Production.Product.ProductID | FK_ProductProductPhoto_Product_ProductID Foreign key constraint referencing Product.ProductID. |
| Production.ProductProductPhoto | - | Production.ProductPhoto | Production.ProductProductPhoto.ProductPhotoID = Production.ProductPhoto.ProductPhotoID | FK_ProductProductPhoto_ProductPhoto_ProductPhotoID Foreign key constraint referencing ProductPhoto.ProductPhotoID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_ProductProductPhoto_ProductID_ProductPhotoID | ProductID, ProductPhotoID | Primary key (clustered) constraint |