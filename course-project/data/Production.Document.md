# Production.Document

> Product maintenance documents.

**Documentation:** AdventureWorks
**Schema:** Production
**Name:** Document
**Module:** Products

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | DocumentNode | hierarchyid | - | - | - | Primary key for Document records. |
| - | 2 | - | DocumentLevel | smallint | - | Computed: [DocumentNode].[GetLevel]() | - | Depth in the document hierarchy. |
| - | 3 | - | Title | nvarchar(50) | - | - | - | Title of the document. |
| - | 4 | - | Owner | int | - | - | - | Employee who controls the document. Foreign key to Employee.BusinessEntityID |
| - | 5 | - | FolderFlag | bit | - | Default: 0 | - | 0 = This is a folder, 1 = This is a document. |
| - | 6 | - | FileName | nvarchar(400) | - | - | - | File name of the document |
| - | 7 | - | FileExtension | nvarchar(8) | - | - | - | File extension indicating the document type. For example, .doc or .txt. |
| - | 8 | - | Revision | nchar(5) | - | - | - | Revision number of the document. |
| - | 9 | - | ChangeNumber | int | - | Default: 0 | - | Engineering change approval number. |
| - | 10 | - | Status | tinyint | - | - | - | 1 = Pending approval, 2 = Approved, 3 = Obsolete |
| - | 11 | - | DocumentSummary | nvarchar(MAX) | - | - | - | Document abstract. |
| - | 12 | - | Document | varbinary(MAX) | - | - | - | Complete document. |
| - | 13 | - | rowguid | uniqueidentifier | - | Default: newid() | - | ROWGUIDCOL number uniquely identifying the record. Required for FileStream. |
| - | 14 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Production.ProductDocument | - | Production.Document | Production.ProductDocument.DocumentNode = Production.Document.DocumentNode | FK_ProductDocument_Document_DocumentNode Foreign key constraint referencing Document.DocumentNode. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_Document_DocumentNode | DocumentNode | Primary key (clustered) constraint |
| - | AK_Document_DocumentLevel_DocumentNode | DocumentLevel, DocumentNode | Unique nonclustered index. |
| - | AK_Document_rowguid | rowguid | Unique nonclustered index. Used to support FileStream. |
| - | UQ__Document__F73921F793071A63 | rowguid | - |