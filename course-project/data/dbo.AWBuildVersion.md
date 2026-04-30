# dbo.AWBuildVersion

> Current version number of the AdventureWorks 2012 sample database.

**Documentation:** AdventureWorks
**Schema:** dbo
**Name:** AWBuildVersion
**Module:** Admin

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | SystemInformationID | tinyint | - | Identity | - | Primary key for AWBuildVersion records. |
| - | 2 | - | Database Version | nvarchar(25) | - | - | - | Version number of the database in 9.yy.mm.dd.00 format. |
| - | 3 | - | VersionDate | datetime | - | - | - | Date and time the record was last updated. |
| - | 4 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_AWBuildVersion_SystemInformationID | SystemInformationID | Primary key (clustered) constraint |