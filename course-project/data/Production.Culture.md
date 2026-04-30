# Production.Culture

> Lookup table containing the languages in which some AdventureWorks data is stored.

**Documentation:** AdventureWorks
**Schema:** Production
**Name:** Culture
**Module:** Products

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | CultureID | nchar(6) | - | - | - | Primary key for Culture records. |
| - | 2 | - | Name | nvarchar(50) | - | - | - | Culture description. |
| - | 3 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Production.ProductModelProductDescriptionCulture | - | Production.Culture | Production.ProductModelProductDescriptionCulture.CultureID = Production.Culture.CultureID | FK_ProductModelProductDescriptionCulture_Culture_CultureID Foreign key constraint referencing Culture.CultureID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_Culture_CultureID | CultureID | Primary key (clustered) constraint |
| - | AK_Culture_Name | Name | Unique nonclustered index. |