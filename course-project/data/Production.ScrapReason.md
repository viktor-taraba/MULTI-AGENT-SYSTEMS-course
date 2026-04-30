# Production.ScrapReason

> Manufacturing failure reasons lookup table.

**Documentation:** AdventureWorks
**Schema:** Production
**Name:** ScrapReason
**Module:** Manufacturing

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | ScrapReasonID | smallint | - | Identity | - | Primary key for ScrapReason records. |
| - | 2 | - | Name | nvarchar(50) | - | - | - | Failure description. |
| - | 3 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Production.WorkOrder | - | Production.ScrapReason | Production.WorkOrder.ScrapReasonID = Production.ScrapReason.ScrapReasonID | FK_WorkOrder_ScrapReason_ScrapReasonID Foreign key constraint referencing ScrapReason.ScrapReasonID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_ScrapReason_ScrapReasonID | ScrapReasonID | Primary key (clustered) constraint |
| - | AK_ScrapReason_Name | Name | Unique nonclustered index. |