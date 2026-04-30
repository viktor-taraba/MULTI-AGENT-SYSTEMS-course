# Sales.SpecialOfferProduct

> Cross-reference table mapping products to special offer discounts.

**Documentation:** AdventureWorks
**Schema:** Sales
**Name:** SpecialOfferProduct
**Module:** Sales

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | SpecialOfferID | int | - | - | Sales.SpecialOffer | Primary key for SpecialOfferProduct records. |
| - | 2 | - | ProductID | int | - | - | Production.Product | Product identification number. Foreign key to Product.ProductID. |
| - | 3 | - | rowguid | uniqueidentifier | - | Default: newid() | - | ROWGUIDCOL number uniquely identifying the record. Used to support a merge replication sample. |
| - | 4 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Sales.SpecialOfferProduct | - | Production.Product | Sales.SpecialOfferProduct.ProductID = Production.Product.ProductID | FK_SpecialOfferProduct_Product_ProductID Foreign key constraint referencing Product.ProductID. |
| Sales.SpecialOfferProduct | - | Sales.SpecialOffer | Sales.SpecialOfferProduct.SpecialOfferID = Sales.SpecialOffer.SpecialOfferID | FK_SpecialOfferProduct_SpecialOffer_SpecialOfferID Foreign key constraint referencing SpecialOffer.SpecialOfferID. |
| Sales.SalesOrderDetail | - | Sales.SpecialOfferProduct | Sales.SalesOrderDetail.SpecialOfferID = Sales.SpecialOfferProduct.SpecialOfferID Sales.SalesOrderDetail.ProductID = Sales.SpecialOfferProduct.ProductID | FK_SalesOrderDetail_SpecialOfferProduct_SpecialOfferIDProductID Foreign key constraint referencing SpecialOfferProduct.SpecialOfferIDProductID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_SpecialOfferProduct_SpecialOfferID_ProductID | SpecialOfferID, ProductID | Primary key (clustered) constraint |
| - | AK_SpecialOfferProduct_rowguid | rowguid | Unique nonclustered index. Used to support replication samples. |