# Purchasing.PurchaseOrderDetail

> Individual products associated with a specific purchase order. See PurchaseOrderHeader.

**Documentation:** AdventureWorks
**Schema:** Purchasing
**Name:** PurchaseOrderDetail
**Module:** Purchasing

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | PurchaseOrderID | int | - | - | Purchasing.PurchaseOrderHeader | Primary key. Foreign key to PurchaseOrderHeader.PurchaseOrderID. |
| - | 2 | - | PurchaseOrderDetailID | int | - | Identity | - | Primary key. One line number per purchased product. |
| - | 3 | - | DueDate | datetime | - | - | - | Date the product is expected to be received. |
| - | 4 | - | OrderQty | smallint | - | - | - | Quantity ordered. |
| - | 5 | - | ProductID | int | - | - | Production.Product | Product identification number. Foreign key to Product.ProductID. |
| - | 6 | - | UnitPrice | money | - | - | - | Vendor's selling price of a single product. |
| - | 7 | - | LineTotal | money | - | Computed: isnull([OrderQty]*[UnitPrice],(0.00)) | - | Per product subtotal. Computed as OrderQty * UnitPrice. |
| - | 8 | - | ReceivedQty | decimal(8, 2) | - | - | - | Quantity actually received from the vendor. |
| - | 9 | - | RejectedQty | decimal(8, 2) | - | - | - | Quantity rejected during inspection. |
| - | 10 | - | StockedQty | decimal(9, 2) | - | Computed: isnull([ReceivedQty]-[RejectedQty],(0.00)) | - | Quantity accepted into inventory. Computed as ReceivedQty - RejectedQty. |
| - | 11 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Purchasing.PurchaseOrderDetail | - | Production.Product | Purchasing.PurchaseOrderDetail.ProductID = Production.Product.ProductID | FK_PurchaseOrderDetail_Product_ProductID Foreign key constraint referencing Product.ProductID. |
| Purchasing.PurchaseOrderDetail | - | Purchasing.PurchaseOrderHeader | Purchasing.PurchaseOrderDetail.PurchaseOrderID = Purchasing.PurchaseOrderHeader.PurchaseOrderID | FK_PurchaseOrderDetail_PurchaseOrderHeader_PurchaseOrderID Foreign key constraint referencing PurchaseOrderHeader.PurchaseOrderID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_PurchaseOrderDetail_PurchaseOrderID_PurchaseOrderDetailID | PurchaseOrderID, PurchaseOrderDetailID | Primary key (clustered) constraint |