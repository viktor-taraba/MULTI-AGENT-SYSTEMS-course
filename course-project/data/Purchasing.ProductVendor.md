# Purchasing.ProductVendor

> Cross-reference table mapping vendors with the products they supply.

**Documentation:** AdventureWorks
**Schema:** Purchasing
**Name:** ProductVendor
**Module:** Purchasing

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | ProductID | int | - | - | Production.Product | Primary key. Foreign key to Product.ProductID. |
| - | 2 | - | BusinessEntityID | int | - | - | Purchasing.Vendor | Primary key. Foreign key to Vendor.BusinessEntityID. |
| - | 3 | - | AverageLeadTime | int | - | - | - | The average span of time (in days) between placing an order with the vendor and receiving the purchased product. |
| - | 4 | - | StandardPrice | money | - | - | - | The vendor's usual selling price. |
| - | 5 | - | LastReceiptCost | money | - | - | - | The selling price when last purchased. |
| - | 6 | - | LastReceiptDate | datetime | - | - | - | Date the product was last received by the vendor. |
| - | 7 | - | MinOrderQty | int | - | - | - | The maximum quantity that should be ordered. |
| - | 8 | - | MaxOrderQty | int | - | - | - | The minimum quantity that should be ordered. |
| - | 9 | - | OnOrderQty | int | - | - | - | The quantity currently on order. |
| - | 10 | - | UnitMeasureCode | nchar(3) | - | - | Production.UnitMeasure | The product's unit of measure. |
| - | 11 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Purchasing.ProductVendor | - | Production.Product | Purchasing.ProductVendor.ProductID = Production.Product.ProductID | FK_ProductVendor_Product_ProductID Foreign key constraint referencing Product.ProductID. |
| Purchasing.ProductVendor | - | Production.UnitMeasure | Purchasing.ProductVendor.UnitMeasureCode = Production.UnitMeasure.UnitMeasureCode | FK_ProductVendor_UnitMeasure_UnitMeasureCode Foreign key constraint referencing UnitMeasure.UnitMeasureCode. |
| Purchasing.ProductVendor | - | Purchasing.Vendor | Purchasing.ProductVendor.BusinessEntityID = Purchasing.Vendor.BusinessEntityID | FK_ProductVendor_Vendor_BusinessEntityID Foreign key constraint referencing Vendor.BusinessEntityID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_ProductVendor_ProductID_BusinessEntityID | ProductID, BusinessEntityID | Primary key (clustered) constraint |