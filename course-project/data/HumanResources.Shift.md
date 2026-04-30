# HumanResources.Shift

> Work shift lookup table.

**Documentation:** AdventureWorks
**Schema:** HumanResources
**Name:** Shift
**Module:** Human Resources

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | ShiftID | tinyint | - | Identity | - | Primary key for Shift records. |
| - | 2 | - | Name | nvarchar(50) | - | - | - | Shift description. |
| - | 3 | - | StartTime | time(7) | - | - | - | Shift start time. |
| - | 4 | - | EndTime | time(7) | - | - | - | Shift end time. |
| - | 5 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| HumanResources.Employee | - | HumanResources.Shift | - | zzz zxczxc |
| HumanResources.EmployeeDepartmentHistory | - | HumanResources.Shift | HumanResources.EmployeeDepartmentHistory.ShiftID = HumanResources.Shift.ShiftID | FK_EmployeeDepartmentHistory_Shift_ShiftID Foreign key constraint referencing Shift.ShiftID |
| HumanResources.vEmployeeDepartmentHistory | - | HumanResources.Shift | HumanResources.vEmployeeDepartmentHistory.Title = HumanResources.Shift.Name | fk_Shift_vEmployeeDepartmentHistory xcbxcvbxcvbbvbvb |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_Shift_ShiftID | ShiftID | Primary key (clustered) constraint |
| - | AK_Shift_Name | Name | Unique nonclustered index. |
| - | AK_Shift_StartTime_EndTime | StartTime, EndTime | Unique nonclustered index. |