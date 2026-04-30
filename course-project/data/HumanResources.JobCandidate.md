# HumanResources.JobCandidate

> Résumés submitted to Human Resources by job applicants.

**Documentation:** AdventureWorks
**Schema:** HumanResources
**Name:** JobCandidate
**Module:** Human Resources

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | JobCandidateID | int | - | Identity | - | Primary key for JobCandidate records. |
| - | 2 | - | BusinessEntityID | int | - | - | HumanResources.Employee | Employee identification number if applicant was hired. Foreign key to Employee.BusinessEntityID. |
| - | 3 | - | Resume | xml | - | - | - | Résumé in XML format. |
| - | 4 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| HumanResources.JobCandidate | - | HumanResources.Employee | HumanResources.JobCandidate.BusinessEntityID = HumanResources.Employee.BusinessEntityID | FK_JobCandidate_Employee_BusinessEntityID Foreign key constraint referencing Employee.EmployeeID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_JobCandidate_JobCandidateID | JobCandidateID | Primary key (clustered) constraint |