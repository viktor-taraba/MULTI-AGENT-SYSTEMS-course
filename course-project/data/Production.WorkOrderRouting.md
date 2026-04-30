# Production.WorkOrderRouting

> Work order details.

**Documentation:** AdventureWorks
**Schema:** Production
**Name:** WorkOrderRouting
**Module:** Manufacturing

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | WorkOrderID | int | - | - | Production.WorkOrder | Primary key. Foreign key to WorkOrder.WorkOrderID. |
| - | 2 | - | ProductID | int | - | - | - | Primary key. Foreign key to Product.ProductID. |
| - | 3 | - | OperationSequence | smallint | - | - | - | Primary key. Indicates the manufacturing process sequence. |
| - | 4 | - | LocationID | smallint | - | - | Production.Location | Manufacturing location where the part is processed. Foreign key to Location.LocationID. |
| - | 5 | - | ScheduledStartDate | datetime | - | - | - | Planned manufacturing start date. |
| - | 6 | - | ScheduledEndDate | datetime | - | - | - | Planned manufacturing end date. |
| - | 7 | - | ActualStartDate | datetime | - | - | - | Actual start date. |
| - | 8 | - | ActualEndDate | datetime | - | - | - | Actual end date. |
| - | 9 | - | ActualResourceHrs | decimal(9, 4) | - | - | - | Number of manufacturing hours used. |
| - | 10 | - | PlannedCost | money | - | - | - | Estimated manufacturing cost. |
| - | 11 | - | ActualCost | money | - | - | - | Actual manufacturing cost. |
| - | 12 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Production.WorkOrderRouting | - | Production.Location | Production.WorkOrderRouting.LocationID = Production.Location.LocationID | FK_WorkOrderRouting_Location_LocationID Foreign key constraint referencing Location.LocationID. |
| Production.WorkOrderRouting | - | Production.WorkOrder | Production.WorkOrderRouting.WorkOrderID = Production.WorkOrder.WorkOrderID | FK_WorkOrderRouting_WorkOrder_WorkOrderID Foreign key constraint referencing WorkOrder.WorkOrderID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_WorkOrderRouting_WorkOrderID_ProductID_OperationSequence | WorkOrderID, ProductID, OperationSequence | Primary key (clustered) constraint |