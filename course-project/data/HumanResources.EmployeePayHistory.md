# HumanResources.EmployeePayHistory

> Employee pay history.

**Documentation:** AdventureWorks
**Schema:** HumanResources
**Name:** EmployeePayHistory
**Module:** Human Resources

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | BusinessEntityID | int | - | - | HumanResources.Employee | Employee identification number. Foreign key to Employee.BusinessEntityID. |
| - | 2 | - | RateChangeDate | datetime | - | - | - | Date the change in pay is effective |
| - | 3 | - | Rate | money | - | - | - | Salary hourly rate. |
| - | 4 | - | PayFrequency | tinyint | - | - | - | 1 = Salary received monthly, 2 = Salary received biweekly |
| - | 5 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| HumanResources.EmployeePayHistory | - | HumanResources.Employee | HumanResources.EmployeePayHistory.BusinessEntityID = HumanResources.Employee.BusinessEntityID | FK_EmployeePayHistory_Employee_BusinessEntityID Foreign key constraint referencing Employee.EmployeeID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_EmployeePayHistory_BusinessEntityID_RateChangeDate | BusinessEntityID, RateChangeDate | Primary key (clustered) constraint |