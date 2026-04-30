# Production.ProductReview

> Customer reviews of products they have purchased.

**Documentation:** AdventureWorks
**Schema:** Production
**Name:** ProductReview
**Module:** Products

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | ProductReviewID | int | - | Identity | - | Primary key for ProductReview records. |
| - | 2 | - | ProductID | int | - | - | Production.Product | Product identification number. Foreign key to Product.ProductID. |
| - | 3 | - | ReviewerName | nvarchar(50) | - | - | - | Name of the reviewer. |
| - | 4 | - | ReviewDate | datetime | - | Default: getdate() | - | Date review was submitted. |
| - | 5 | - | EmailAddress | nvarchar(50) | - | - | - | Reviewer's e-mail address. |
| - | 6 | - | Rating | int | - | - | - | Product rating given by the reviewer. Scale is 1 to 5 with 5 as the highest rating. |
| - | 7 | - | Comments | nvarchar(3850) | - | - | - | Reviewer's comments |
| - | 8 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Production.ProductReview | - | Production.Product | Production.ProductReview.ProductID = Production.Product.ProductID | FK_ProductReview_Product_ProductID Foreign key constraint referencing Product.ProductID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_ProductReview_ProductReviewID | ProductReviewID | Primary key (clustered) constraint |