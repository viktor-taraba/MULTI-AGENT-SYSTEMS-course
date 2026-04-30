# Production.ProductPhoto

> Product images.

**Documentation:** AdventureWorks
**Schema:** Production
**Name:** ProductPhoto
**Module:** Products

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | ProductPhotoID | int | - | Identity | - | Primary key for ProductPhoto records. |
| - | 2 | - | ThumbNailPhoto | varbinary(MAX) | - | - | - | Small image of the product. |
| - | 3 | - | ThumbnailPhotoFileName | nvarchar(50) | - | - | - | Small image file name. |
| - | 4 | - | LargePhoto | varbinary(MAX) | - | - | - | Large image of the product. |
| - | 5 | - | LargePhotoFileName | nvarchar(50) | - | - | - | Large image file name. |
| - | 6 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Production.ProductProductPhoto | - | Production.ProductPhoto | Production.ProductProductPhoto.ProductPhotoID = Production.ProductPhoto.ProductPhotoID | FK_ProductProductPhoto_ProductPhoto_ProductPhotoID Foreign key constraint referencing ProductPhoto.ProductPhotoID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_ProductPhoto_ProductPhotoID | ProductPhotoID | Primary key (clustered) constraint |