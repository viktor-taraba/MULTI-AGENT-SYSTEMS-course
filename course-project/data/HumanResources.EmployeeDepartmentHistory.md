# HumanResources.EmployeeDepartmentHistory

> Employee department transfers.

**Documentation:** AdventureWorks
**Schema:** HumanResources
**Name:** EmployeeDepartmentHistory
**Module:** Human Resources

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | BusinessEntityID | int | - | - | HumanResources.Employee | Employee identification number. Foreign key to Employee.BusinessEntityID. |
| - | 2 | - | DepartmentID | smallint | - | - | HumanResources.Department | Department in which the employee worked including currently. Foreign key to Department.DepartmentID. |
| - | 3 | - | ShiftID | tinyint | - | - | HumanResources.Shift | Identifies which 8-hour shift the employee works. Foreign key to Shift.Shift.ID. |
| - | 4 | - | StartDate | date | - | - | - | Date the employee started work in the department. |
| - | 5 | - | EndDate | date | - | - | - | Date the employee left the department. NULL = Current department. |
| - | 6 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| HumanResources.EmployeeDepartmentHistory | - | HumanResources.Department | HumanResources.EmployeeDepartmentHistory.DepartmentID = HumanResources.Department.DepartmentID | FK_EmployeeDepartmentHistory_Department_DepartmentID Foreign key constraint referencing Department.DepartmentID. |
| HumanResources.EmployeeDepartmentHistory | - | HumanResources.Employee | HumanResources.EmployeeDepartmentHistory.BusinessEntityID = HumanResources.Employee.BusinessEntityID | FK_EmployeeDepartmentHistory_Employee_BusinessEntityID Foreign key constraint referencing Employee.EmployeeID. |
| HumanResources.EmployeeDepartmentHistory | - | HumanResources.Shift | HumanResources.EmployeeDepartmentHistory.ShiftID = HumanResources.Shift.ShiftID | FK_EmployeeDepartmentHistory_Shift_ShiftID Foreign key constraint referencing Shift.ShiftID |
| HumanResources.Employee | - | HumanResources.EmployeeDepartmentHistory | - | sdsdsd fk_EmployeeDepartmentHistory_Employee |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_EmployeeDepartmentHistory_BusinessEntityID_StartDate_DepartmentID | BusinessEntityID, DepartmentID, ShiftID, StartDate | Primary key (clustered) constraint |