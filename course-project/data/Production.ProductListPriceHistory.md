# Production.ProductListPriceHistory

> Changes in the list price of a product over time.

**Documentation:** AdventureWorks
**Schema:** Production
**Name:** ProductListPriceHistory
**Module:** Manufacturing

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | ProductID | int | - | - | Production.Product | Product identification number. Foreign key to Product.ProductID |
| - | 2 | - | StartDate | datetime | - | - | - | List price start date. |
| - | 3 | - | EndDate | datetime | - | - | - | List price end date |
| - | 4 | - | ListPrice | money | - | - | - | Product list price. |
| - | 5 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Production.ProductListPriceHistory | - | Production.Product | Production.ProductListPriceHistory.ProductID = Production.Product.ProductID | FK_ProductListPriceHistory_Product_ProductID Foreign key constraint referencing Product.ProductID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_ProductListPriceHistory_ProductID_StartDate | ProductID, StartDate | Primary key (clustered) constraint |