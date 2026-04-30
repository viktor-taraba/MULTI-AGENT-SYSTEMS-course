# Production.Product

> Products sold or used in the manfacturing of sold products.

**Documentation:** AdventureWorks
**Schema:** Production
**Name:** Product
**Module:** Products

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | ProductID | int | - | Identity | - | Primary key for Product records. |
| - | 2 | - | Name | nvarchar(50) | - | - | - | Name of the product. |
| - | 3 | - | ProductNumber | nvarchar(25) | - | - | - | Unique product identification number. |
| - | 4 | - | MakeFlag | bit | - | Default: 1 | - | 0 = Product is purchased, 1 = Product is manufactured in-house. |
| - | 5 | - | FinishedGoodsFlag | bit | - | Default: 1 | - | 0 = Product is not a salable item. 1 = Product is salable. |
| - | 6 | - | Color | nvarchar(15) | - | - | - | Product color. |
| - | 7 | - | SafetyStockLevel | smallint | - | - | - | Minimum inventory quantity. |
| - | 8 | - | ReorderPoint | smallint | - | - | - | Inventory level that triggers a purchase order or work order. |
| - | 9 | - | StandardCost | money | - | - | - | Standard cost of the product. |
| - | 10 | - | ListPrice | money | - | - | - | Selling price. |
| - | 11 | - | Size | nvarchar(5) | - | - | - | Product size. |
| - | 12 | - | SizeUnitMeasureCode | nchar(3) | - | - | Production.UnitMeasure | Unit of measure for Size column. |
| - | 13 | - | WeightUnitMeasureCode | nchar(3) | - | - | Production.UnitMeasure | Unit of measure for Weight column. |
| - | 14 | - | Weight | decimal(8, 2) | - | - | - | Product weight. |
| - | 15 | - | DaysToManufacture | int | - | - | - | Number of days required to manufacture the product. |
| - | 16 | - | ProductLine | nchar(2) | - | - | - | R = Road, M = Mountain, T = Touring, S = Standard |
| - | 17 | - | Class | nchar(2) | - | - | - | H = High, M = Medium, L = Low |
| - | 18 | - | Style | nchar(2) | - | - | - | W = Womens, M = Mens, U = Universal |
| - | 19 | - | ProductSubcategoryID | int | - | - | Production.ProductSubcategory | Product is a member of this product subcategory. Foreign key to ProductSubCategory.ProductSubCategoryID. |
| - | 20 | - | ProductModelID | int | - | - | Production.ProductModel | Product is a member of this product model. Foreign key to ProductModel.ProductModelID. |
| - | 21 | - | SellStartDate | datetime | - | - | - | Date the product was available for sale. |
| - | 22 | - | SellEndDate | datetime | - | - | - | Date the product was no longer available for sale. |
| - | 23 | - | DiscontinuedDate | datetime | - | - | - | Date the product was discontinued. |
| - | 24 | - | rowguid | uniqueidentifier | - | Default: newid() | - | ROWGUIDCOL number uniquely identifying the record. Used to support a merge replication sample. |
| - | 25 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Production.Product | - | Production.ProductModel | Production.Product.ProductModelID = Production.ProductModel.ProductModelID | FK_Product_ProductModel_ProductModelID Foreign key constraint referencing ProductModel.ProductModelID. |
| Production.Product | - | Production.ProductSubcategory | Production.Product.ProductSubcategoryID = Production.ProductSubcategory.ProductSubcategoryID | FK_Product_ProductSubcategory_ProductSubcategoryID Foreign key constraint referencing ProductSubcategory.ProductSubcategoryID. |
| Production.Product | - | Production.UnitMeasure | Production.Product.SizeUnitMeasureCode = Production.UnitMeasure.UnitMeasureCode | FK_Product_UnitMeasure_SizeUnitMeasureCode Foreign key constraint referencing UnitMeasure.UnitMeasureCode. |
| Production.Product | - | Production.UnitMeasure | Production.Product.WeightUnitMeasureCode = Production.UnitMeasure.UnitMeasureCode | FK_Product_UnitMeasure_WeightUnitMeasureCode Foreign key constraint referencing UnitMeasure.UnitMeasureCode. |
| Production.BillOfMaterials | - | Production.Product | Production.BillOfMaterials.ComponentID = Production.Product.ProductID | FK_BillOfMaterials_Product_ComponentID Foreign key constraint referencing Product.ProductAssemblyID. |
| Production.BillOfMaterials | - | Production.Product | Production.BillOfMaterials.ProductAssemblyID = Production.Product.ProductID | FK_BillOfMaterials_Product_ProductAssemblyID Foreign key constraint referencing Product.ProductAssemblyID. |
| Production.ProductCostHistory | - | Production.Product | Production.ProductCostHistory.ProductID = Production.Product.ProductID | FK_ProductCostHistory_Product_ProductID Foreign key constraint referencing Product.ProductID. |
| Production.ProductDocument | - | Production.Product | Production.ProductDocument.ProductID = Production.Product.ProductID | FK_ProductDocument_Product_ProductID Foreign key constraint referencing Product.ProductID. |
| Production.ProductInventory | - | Production.Product | Production.ProductInventory.ProductID = Production.Product.ProductID | FK_ProductInventory_Product_ProductID Foreign key constraint referencing Product.ProductID. |
| Production.ProductListPriceHistory | - | Production.Product | Production.ProductListPriceHistory.ProductID = Production.Product.ProductID | FK_ProductListPriceHistory_Product_ProductID Foreign key constraint referencing Product.ProductID. |
| Production.ProductProductPhoto | - | Production.Product | Production.ProductProductPhoto.ProductID = Production.Product.ProductID | FK_ProductProductPhoto_Product_ProductID Foreign key constraint referencing Product.ProductID. |
| Production.ProductReview | - | Production.Product | Production.ProductReview.ProductID = Production.Product.ProductID | FK_ProductReview_Product_ProductID Foreign key constraint referencing Product.ProductID. |
| Purchasing.ProductVendor | - | Production.Product | Purchasing.ProductVendor.ProductID = Production.Product.ProductID | FK_ProductVendor_Product_ProductID Foreign key constraint referencing Product.ProductID. |
| Purchasing.PurchaseOrderDetail | - | Production.Product | Purchasing.PurchaseOrderDetail.ProductID = Production.Product.ProductID | FK_PurchaseOrderDetail_Product_ProductID Foreign key constraint referencing Product.ProductID. |
| Sales.SalesOrderDetail | - | Production.Product | Sales.SalesOrderDetail.ProductID = Production.Product.ProductID | User-defined relation |
| Sales.ShoppingCartItem | - | Production.Product | Sales.ShoppingCartItem.ProductID = Production.Product.ProductID | FK_ShoppingCartItem_Product_ProductID Foreign key constraint referencing Product.ProductID. |
| Sales.SpecialOfferProduct | - | Production.Product | Sales.SpecialOfferProduct.ProductID = Production.Product.ProductID | FK_SpecialOfferProduct_Product_ProductID Foreign key constraint referencing Product.ProductID. |
| Production.TransactionHistory | - | Production.Product | Production.TransactionHistory.ProductID = Production.Product.ProductID | FK_TransactionHistory_Product_ProductID Foreign key constraint referencing Product.ProductID. |
| Production.TransactionHistoryArchive | - | Production.Product | Production.TransactionHistoryArchive.ProductID = Production.Product.ProductID | User-defined relation |
| Production.WorkOrder | - | Production.Product | Production.WorkOrder.ProductID = Production.Product.ProductID | FK_WorkOrder_Product_ProductID Foreign key constraint referencing Product.ProductID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_Product_ProductID | ProductID | Primary key (clustered) constraint |
| - | AK_Product_Name | Name | Unique nonclustered index. |
| - | AK_Product_ProductNumber | ProductNumber | Unique nonclustered index. |
| - | AK_Product_rowguid | rowguid | Unique nonclustered index. Used to support replication samples. |