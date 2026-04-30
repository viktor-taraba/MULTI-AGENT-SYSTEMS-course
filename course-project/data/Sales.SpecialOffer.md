# Sales.SpecialOffer

> Sale discounts lookup table.

**Documentation:** AdventureWorks
**Schema:** Sales
**Name:** SpecialOffer
**Module:** Sales

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | SpecialOfferID | int | - | Identity | - | Primary key for SpecialOffer records. |
| - | 2 | - | Description | nvarchar(255) | - | - | - | Discount description. |
| - | 3 | - | DiscountPct | smallmoney | - | Default: 0.00 | - | Discount precentage. |
| - | 4 | - | Type | nvarchar(50) | - | - | - | Discount type category. |
| - | 5 | - | Category | nvarchar(50) | - | - | - | Group the discount applies to such as Reseller or Customer. |
| - | 6 | - | StartDate | datetime | - | - | - | Discount start date. |
| - | 7 | - | EndDate | datetime | - | - | - | Discount end date. |
| - | 8 | - | MinQty | int | - | Default: 0 | - | Minimum discount percent allowed. |
| - | 9 | - | MaxQty | int | - | - | - | Maximum discount percent allowed. |
| - | 10 | - | rowguid | uniqueidentifier | - | Default: newid() | - | ROWGUIDCOL number uniquely identifying the record. Used to support a merge replication sample. |
| - | 11 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Sales.SpecialOfferProduct | - | Sales.SpecialOffer | Sales.SpecialOfferProduct.SpecialOfferID = Sales.SpecialOffer.SpecialOfferID | FK_SpecialOfferProduct_SpecialOffer_SpecialOfferID Foreign key constraint referencing SpecialOffer.SpecialOfferID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_SpecialOffer_SpecialOfferID | SpecialOfferID | Primary key (clustered) constraint |
| - | AK_SpecialOffer_rowguid | rowguid | Unique nonclustered index. Used to support replication samples. |