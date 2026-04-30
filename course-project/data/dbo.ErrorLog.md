# dbo.ErrorLog

> Audit table tracking errors in the the AdventureWorks database that are caught by the CATCH block of a TRY...CATCH construct. Data is inserted by stored procedure dbo.uspLogError when it is executed from inside the CATCH block of a TRY...CATCH construct.

**Documentation:** AdventureWorks
**Schema:** dbo
**Name:** ErrorLog
**Module:** Admin

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | ErrorLogID | int | - | Identity | - | Primary key for ErrorLog records. |
| - | 2 | - | ErrorTime | datetime | - | Default: getdate() | - | The date and time at which the error occurred. |
| - | 3 | - | UserName | nvarchar(128) | - | - | - | The user who executed the batch in which the error occurred. |
| - | 4 | - | ErrorNumber | int | - | - | - | The error number of the error that occurred. |
| - | 5 | - | ErrorSeverity | int | - | - | - | The severity of the error that occurred. |
| - | 6 | - | ErrorState | int | - | - | - | The state number of the error that occurred. |
| - | 7 | - | ErrorProcedure | nvarchar(126) | - | - | - | The name of the stored procedure or trigger where the error occurred. |
| - | 8 | - | ErrorLine | int | - | - | - | The line number at which the error occurred. |
| - | 9 | - | ErrorMessage | nvarchar(4000) | - | - | - | The message text of the error that occurred. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_ErrorLog_ErrorLogID | ErrorLogID | Primary key (clustered) constraint |