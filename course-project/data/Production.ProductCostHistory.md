# Production.ProductCostHistory

> Changes in the cost of a product over time.

**Documentation:** AdventureWorks
**Schema:** Production
**Name:** ProductCostHistory
**Module:** Manufacturing

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | ProductID | int | - | - | Production.Product | Product identification number. Foreign key to Product.ProductID |
| - | 2 | - | StartDate | datetime | - | - | - | Product cost start date. |
| - | 3 | - | EndDate | datetime | - | - | - | Product cost end date. |
| - | 4 | - | StandardCost | money | - | - | - | Standard cost of the product. |
| - | 5 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Production.ProductCostHistory | - | Production.Product | Production.ProductCostHistory.ProductID = Production.Product.ProductID | FK_ProductCostHistory_Product_ProductID Foreign key constraint referencing Product.ProductID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_ProductCostHistory_ProductID_StartDate | ProductID, StartDate | Primary key (clustered) constraint |