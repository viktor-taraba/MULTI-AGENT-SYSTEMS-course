# HumanResources.Employee

> Employee information such as salary, department, and title.

**Documentation:** AdventureWorks
**Schema:** HumanResources
**Name:** Employee
**Module:** Human Resources

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | BusinessEntityID | int | - | - | Person.Person | Primary key for Employee records. Foreign key to BusinessEntity.BusinessEntityID. |
| - | 2 | - | NationalIDNumber | nvarchar(15) | - | - | - | Unique national identification number such as a social security number. |
| - | 3 | - | LoginID | nvarchar(256) | - | - | - | Network login. Test2 |
| - | 4 | - | OrganizationNode | hierarchyid | - | - | - | Where the employee is located in corporate hierarchy. |
| - | 5 | - | OrganizationLevel | smallint | - | Computed: [OrganizationNode].[GetLevel]() | - | The depth of the employee in the corporate hierarchy. |
| - | 6 | - | JobTitle | nvarchar(50) | - | - | - | Work title such as Buyer or Sales Representative. |
| - | 7 | - | BirthDate | date | - | - | - | Date of birth. |
| - | 8 | - | MaritalStatus | nchar(1) | - | - | - | M = Married, S = Single |
| - | 9 | - | Gender | nchar(1) | - | - | - | M = Male, F = Female |
| - | 10 | - | HireDate | date | - | - | - | Employee hired on this date. |
| - | 11 | - | SalariedFlag | bit | - | Default: 1 | - | Job classification. 0 = Hourly, not exempt from collective bargaining. 1 = Salaried, exempt from collective bargaining. |
| - | 12 | - | VacationHours | smallint | - | Default: 0 | - | Number of available vacation hours. |
| - | 13 | - | SickLeaveHours | smallint | - | Default: 0 | - | Number of available sick leave hours. |
| - | 14 | - | CurrentFlag | bit | - | Default: 1 | - | 0 = Inactive, 1 = Active |
| - | 15 | - | rowguid | uniqueidentifier | - | Default: newid() | - | ROWGUIDCOL number uniquely identifying the record. Used to support a merge replication sample. |
| - | 16 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| HumanResources.Employee | - | HumanResources.EmployeeDepartmentHistory | - | sdsdsd fk_EmployeeDepartmentHistory_Employee |
| HumanResources.Employee | - | Person.Person | HumanResources.Employee.BusinessEntityID = Person.Person.BusinessEntityID | FK_Employee_Person_BusinessEntityID Foreign key constraint referencing Person.BusinessEntityID. |
| HumanResources.Employee | - | HumanResources.Shift | - | zzz zxczxc |
| HumanResources.Employee | - | HumanResources.vEmployeeDepartment | - | qqq asdasda |
| HumanResources.EmployeeDepartmentHistory | - | HumanResources.Employee | HumanResources.EmployeeDepartmentHistory.BusinessEntityID = HumanResources.Employee.BusinessEntityID | FK_EmployeeDepartmentHistory_Employee_BusinessEntityID Foreign key constraint referencing Employee.EmployeeID. |
| HumanResources.EmployeePayHistory | - | HumanResources.Employee | HumanResources.EmployeePayHistory.BusinessEntityID = HumanResources.Employee.BusinessEntityID | FK_EmployeePayHistory_Employee_BusinessEntityID Foreign key constraint referencing Employee.EmployeeID. |
| HumanResources.JobCandidate | - | HumanResources.Employee | HumanResources.JobCandidate.BusinessEntityID = HumanResources.Employee.BusinessEntityID | FK_JobCandidate_Employee_BusinessEntityID Foreign key constraint referencing Employee.EmployeeID. |
| Purchasing.PurchaseOrderHeader | - | HumanResources.Employee | Purchasing.PurchaseOrderHeader.EmployeeID = HumanResources.Employee.BusinessEntityID | FK_PurchaseOrderHeader_Employee_EmployeeID Foreign key constraint referencing Employee.EmployeeID. |
| Sales.SalesPerson | - | HumanResources.Employee | Sales.SalesPerson.BusinessEntityID = HumanResources.Employee.BusinessEntityID | FK_SalesPerson_Employee_BusinessEntityID Foreign key constraint referencing Employee.EmployeeID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_Employee_BusinessEntityID | BusinessEntityID | Primary key (clustered) constraint |
| - | fvxzcvbxb | BirthDate | cxvbxcvbvbvcb |
| - | AK_Employee_LoginID | LoginID | Unique nonclustered index. |
| - | AK_Employee_NationalIDNumber | NationalIDNumber | Unique nonclustered index. |
| - | AK_Employee_rowguid | rowguid | Unique nonclustered index. Used to support replication samples. |