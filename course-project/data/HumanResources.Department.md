# HumanResources.Department

> Lookup table containing the departments within the Adventure Works Cycles company.

**Documentation:** AdventureWorks
**Schema:** HumanResources
**Name:** Department
**Module:** Human Resources

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | DepartmentID | smallint | - | Identity | - | Primary key for Department records. |
| - | 2 | - | Name | nvarchar(50) | - | - | - | Name of the department. |
| - | 3 | - | GroupName | nvarchar(50) | - | - | - | Name of the group to which the department belongs. |
| - | 4 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| HumanResources.EmployeeDepartmentHistory | - | HumanResources.Department | HumanResources.EmployeeDepartmentHistory.DepartmentID = HumanResources.Department.DepartmentID | FK_EmployeeDepartmentHistory_Department_DepartmentID Foreign key constraint referencing Department.DepartmentID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_Department_DepartmentID | DepartmentID | Primary key (clustered) constraint |
| - | AK_Department_Name | Name | Unique nonclustered index. |