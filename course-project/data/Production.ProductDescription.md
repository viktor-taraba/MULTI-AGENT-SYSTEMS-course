# Production.ProductDescription

> Product descriptions in several languages.

**Documentation:** AdventureWorks
**Schema:** Production
**Name:** ProductDescription
**Module:** Products

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | ProductDescriptionID | int | - | Identity | - | Primary key for ProductDescription records. |
| - | 2 | - | Description | nvarchar(400) | - | - | - | Description of the product. |
| - | 3 | - | rowguid | uniqueidentifier | - | Default: newid() | Production.Illustration | ROWGUIDCOL number uniquely identifying the record. Used to support a merge replication sample. |
| - | 4 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Production.ProductDescription | - | Production.Illustration | Production.ProductDescription.rowguid = Production.Illustration.IllustrationID | fk_Illustration_ProductDescription |
| Production.ProductModelProductDescriptionCulture | - | Production.ProductDescription | Production.ProductModelProductDescriptionCulture.ProductDescriptionID = Production.ProductDescription.ProductDescriptionID | FK_ProductModelProductDescriptionCulture_ProductDescription_ProductDescriptionID Foreign key constraint referencing ProductDescription.ProductDescriptionID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_ProductDescription_ProductDescriptionID | ProductDescriptionID | Primary key (clustered) constraint |
| - | AK_ProductDescription_rowguid | rowguid | Unique nonclustered index. Used to support replication samples. |