# Production.ProductInventory

> Product inventory information.

**Documentation:** AdventureWorks
**Schema:** Production
**Name:** ProductInventory
**Module:** Inventory

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | ProductID | int | - | - | Production.Product | Product identification number. Foreign key to Product.ProductID. |
| - | 2 | - | LocationID | smallint | - | - | Production.Location | Inventory location identification number. Foreign key to Location.LocationID. |
| - | 3 | - | Shelf | nvarchar(10) | - | - | - | Storage compartment within an inventory location. |
| - | 4 | - | Bin | tinyint | - | - | - | Storage container on a shelf in an inventory location. |
| - | 5 | - | Quantity | smallint | - | Default: 0 | - | Quantity of products in the inventory location. |
| - | 6 | - | rowguid | uniqueidentifier | - | Default: newid() | - | ROWGUIDCOL number uniquely identifying the record. Used to support a merge replication sample. |
| - | 7 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Production.ProductInventory | - | Production.Location | Production.ProductInventory.LocationID = Production.Location.LocationID | FK_ProductInventory_Location_LocationID Foreign key constraint referencing Location.LocationID. |
| Production.ProductInventory | - | Production.Product | Production.ProductInventory.ProductID = Production.Product.ProductID | FK_ProductInventory_Product_ProductID Foreign key constraint referencing Product.ProductID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_ProductInventory_ProductID_LocationID | ProductID, LocationID | Primary key (clustered) constraint |