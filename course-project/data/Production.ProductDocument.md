# Production.ProductDocument

> Cross-reference table mapping products to related product documents.

**Documentation:** AdventureWorks
**Schema:** Production
**Name:** ProductDocument
**Module:** Products

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | ProductID | int | - | - | Production.Product | Product identification number. Foreign key to Product.ProductID. |
| - | 2 | - | DocumentNode | hierarchyid | - | - | Production.Document | Document identification number. Foreign key to Document.DocumentNode. |
| - | 3 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Production.ProductDocument | - | Production.Document | Production.ProductDocument.DocumentNode = Production.Document.DocumentNode | FK_ProductDocument_Document_DocumentNode Foreign key constraint referencing Document.DocumentNode. |
| Production.ProductDocument | - | Production.Product | Production.ProductDocument.ProductID = Production.Product.ProductID | FK_ProductDocument_Product_ProductID Foreign key constraint referencing Product.ProductID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_ProductDocument_ProductID_DocumentNode | ProductID, DocumentNode | Primary key (clustered) constraint |