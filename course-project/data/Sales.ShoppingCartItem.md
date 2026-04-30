# Sales.ShoppingCartItem

> Contains online customer orders until the order is submitted or cancelled.

**Documentation:** AdventureWorks
**Schema:** Sales
**Name:** ShoppingCartItem
**Module:** Sales

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | ShoppingCartItemID | int | - | Identity | - | Primary key for ShoppingCartItem records. |
| - | 2 | - | ShoppingCartID | nvarchar(50) | - | - | - | Shopping cart identification number. |
| - | 3 | - | Quantity | int | - | Default: 1 | - | Product quantity ordered. |
| - | 4 | - | ProductID | int | - | - | Production.Product | Product ordered. Foreign key to Product.ProductID. |
| - | 5 | - | DateCreated | datetime | - | Default: getdate() | - | Date the time the record was created. |
| - | 6 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Sales.ShoppingCartItem | - | Production.Product | Sales.ShoppingCartItem.ProductID = Production.Product.ProductID | FK_ShoppingCartItem_Product_ProductID Foreign key constraint referencing Product.ProductID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_ShoppingCartItem_ShoppingCartItemID | ShoppingCartItemID | Primary key (clustered) constraint |