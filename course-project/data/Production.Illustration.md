# Production.Illustration

> Bicycle assembly diagrams.

**Documentation:** AdventureWorks
**Schema:** Production
**Name:** Illustration
**Module:** Products

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | IllustrationID | int | - | Identity | - | Primary key for Illustration records. |
| - | 2 | - | Diagram | xml | - | - | - | Illustrations used in manufacturing instructions. Stored as XML. |
| - | 3 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Production.ProductDescription | - | Production.Illustration | Production.ProductDescription.rowguid = Production.Illustration.IllustrationID | fk_Illustration_ProductDescription |
| Production.ProductModelIllustration | - | Production.Illustration | Production.ProductModelIllustration.IllustrationID = Production.Illustration.IllustrationID | FK_ProductModelIllustration_Illustration_IllustrationID Foreign key constraint referencing Illustration.IllustrationID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_Illustration_IllustrationID | IllustrationID | Primary key (clustered) constraint |