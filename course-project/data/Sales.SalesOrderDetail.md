# Sales.SalesOrderDetail

> Individual products associated with a specific sales order. See SalesOrderHeader.

**Documentation:** AdventureWorks
**Schema:** Sales
**Name:** SalesOrderDetail
**Module:** Sales

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | SalesOrderID | int | - | - | Sales.SalesOrderHeader | Primary key. Foreign key to SalesOrderHeader.SalesOrderID. |
| - | 2 | - | SalesOrderDetailID | int | - | Identity | - | Primary key. One incremental unique number per product sold. |
| - | 3 | - | CarrierTrackingNumber | nvarchar(25) | - | - | - | Shipment tracking number supplied by the shipper. |
| - | 4 | - | OrderQty | smallint | - | - | - | Quantity ordered per product. |
| - | 5 | - | ProductID | int | - | - | Production.Product Sales.SpecialOfferProduct | Product sold to customer. Foreign key to Product.ProductID. |
| - | 6 | - | SpecialOfferID | int | - | - | Sales.SpecialOfferProduct | Promotional code. Foreign key to SpecialOffer.SpecialOfferID. |
| - | 7 | - | UnitPrice | money | - | - | - | Selling price of a single product. |
| - | 8 | - | UnitPriceDiscount | money | - | Default: 0.0 | - | Discount amount. |
| - | 9 | - | LineTotal | numeric(38, 6) | - | Computed: isnull(([UnitPrice]*((1.0)-[UnitPriceDiscount]))*[OrderQty],(0.0)) | - | Per product subtotal. Computed as UnitPrice * (1 - UnitPriceDiscount) * OrderQty. |
| - | 10 | - | rowguid | uniqueidentifier | - | Default: newid() | - | ROWGUIDCOL number uniquely identifying the record. Used to support a merge replication sample. |
| - | 11 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Sales.SalesOrderDetail | - | Production.Product | Sales.SalesOrderDetail.ProductID = Production.Product.ProductID | User-defined relation |
| Sales.SalesOrderDetail | - | Sales.SalesOrderHeader | Sales.SalesOrderDetail.SalesOrderID = Sales.SalesOrderHeader.SalesOrderID | FK_SalesOrderDetail_SalesOrderHeader_SalesOrderID Foreign key constraint referencing SalesOrderHeader.PurchaseOrderID. |
| Sales.SalesOrderDetail | - | Sales.SpecialOfferProduct | Sales.SalesOrderDetail.SpecialOfferID = Sales.SpecialOfferProduct.SpecialOfferID Sales.SalesOrderDetail.ProductID = Sales.SpecialOfferProduct.ProductID | FK_SalesOrderDetail_SpecialOfferProduct_SpecialOfferIDProductID Foreign key constraint referencing SpecialOfferProduct.SpecialOfferIDProductID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_SalesOrderDetail_SalesOrderID_SalesOrderDetailID | SalesOrderID, SalesOrderDetailID | Primary key (clustered) constraint |
| - | AK_SalesOrderDetail_rowguid | rowguid | Unique nonclustered index. Used to support replication samples. |