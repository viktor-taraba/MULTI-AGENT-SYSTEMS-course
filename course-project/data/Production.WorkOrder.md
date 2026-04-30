# Production.WorkOrder

> Manufacturing work orders.

**Documentation:** AdventureWorks
**Schema:** Production
**Name:** WorkOrder
**Module:** Manufacturing

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | WorkOrderID | int | - | Identity | - | Primary key for WorkOrder records. |
| - | 2 | - | ProductID | int | - | - | Production.Product | Product identification number. Foreign key to Product.ProductID. |
| - | 3 | - | OrderQty | int | - | - | - | Product quantity to build. |
| - | 4 | - | StockedQty | int | - | Computed: isnull([OrderQty]-[ScrappedQty],(0)) | - | Quantity built and put in inventory. |
| - | 5 | - | ScrappedQty | smallint | - | - | - | Quantity that failed inspection. |
| - | 6 | - | StartDate | datetime | - | - | - | Work order start date. |
| - | 7 | - | EndDate | datetime | - | - | - | Work order end date. |
| - | 8 | - | DueDate | datetime | - | - | - | Work order due date. |
| - | 9 | - | ScrapReasonID | smallint | - | - | Production.ScrapReason | Reason for inspection failure. |
| - | 10 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Production.WorkOrder | - | Production.Product | Production.WorkOrder.ProductID = Production.Product.ProductID | FK_WorkOrder_Product_ProductID Foreign key constraint referencing Product.ProductID. |
| Production.WorkOrder | - | Production.ScrapReason | Production.WorkOrder.ScrapReasonID = Production.ScrapReason.ScrapReasonID | FK_WorkOrder_ScrapReason_ScrapReasonID Foreign key constraint referencing ScrapReason.ScrapReasonID. |
| Production.WorkOrderRouting | - | Production.WorkOrder | Production.WorkOrderRouting.WorkOrderID = Production.WorkOrder.WorkOrderID | FK_WorkOrderRouting_WorkOrder_WorkOrderID Foreign key constraint referencing WorkOrder.WorkOrderID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_WorkOrder_WorkOrderID | WorkOrderID | Primary key (clustered) constraint |