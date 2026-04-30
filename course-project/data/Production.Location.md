# Production.Location

> Product inventory and manufacturing locations.

**Documentation:** AdventureWorks
**Schema:** Production
**Name:** Location
**Module:** Inventory

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | LocationID | smallint | - | Identity | - | Primary key for Location records. |
| - | 2 | - | Name | nvarchar(50) | - | - | - | Location description. |
| - | 3 | - | CostRate | smallmoney | - | Default: 0.00 | - | Standard hourly cost of the manufacturing location. |
| - | 4 | - | Availability | decimal(8, 2) | - | Default: 0.00 | - | Work capacity (in hours) of the manufacturing location. |
| - | 5 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Production.ProductInventory | - | Production.Location | Production.ProductInventory.LocationID = Production.Location.LocationID | FK_ProductInventory_Location_LocationID Foreign key constraint referencing Location.LocationID. |
| Production.WorkOrderRouting | - | Production.Location | Production.WorkOrderRouting.LocationID = Production.Location.LocationID | FK_WorkOrderRouting_Location_LocationID Foreign key constraint referencing Location.LocationID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_Location_LocationID | LocationID | Primary key (clustered) constraint |
| - | AK_Location_Name | Name | Unique nonclustered index. |