# Purchasing.Vendor

> Companies from whom Adventure Works Cycles purchases parts or other goods.

**Documentation:** AdventureWorks
**Schema:** Purchasing
**Name:** Vendor
**Module:** Purchasing

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | BusinessEntityID | int | - | - | Person.BusinessEntity | Primary key for Vendor records. Foreign key to BusinessEntity.BusinessEntityID |
| - | 2 | - | AccountNumber | nvarchar(15) | - | - | - | Vendor account (identification) number. |
| - | 3 | - | Name | nvarchar(50) | - | - | - | Company name. |
| - | 4 | - | CreditRating | tinyint | - | - | - | 1 = Superior, 2 = Excellent, 3 = Above average, 4 = Average, 5 = Below average |
| - | 5 | - | PreferredVendorStatus | bit | - | Default: 1 | - | 0 = Do not use if another vendor is available. 1 = Preferred over other vendors supplying the same product. |
| - | 6 | - | ActiveFlag | bit | - | Default: 1 | - | 0 = Vendor no longer used. 1 = Vendor is actively used. |
| - | 7 | - | PurchasingWebServiceURL | nvarchar(1024) | - | - | - | Vendor URL. |
| - | 8 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Purchasing.Vendor | - | Person.BusinessEntity | Purchasing.Vendor.BusinessEntityID = Person.BusinessEntity.BusinessEntityID | FK_Vendor_BusinessEntity_BusinessEntityID Foreign key constraint referencing BusinessEntity.BusinessEntityID |
| Purchasing.ProductVendor | - | Purchasing.Vendor | Purchasing.ProductVendor.BusinessEntityID = Purchasing.Vendor.BusinessEntityID | FK_ProductVendor_Vendor_BusinessEntityID Foreign key constraint referencing Vendor.BusinessEntityID. |
| Purchasing.PurchaseOrderHeader | - | Purchasing.Vendor | Purchasing.PurchaseOrderHeader.VendorID = Purchasing.Vendor.BusinessEntityID | FK_PurchaseOrderHeader_Vendor_VendorID Foreign key constraint referencing Vendor.VendorID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_Vendor_BusinessEntityID | BusinessEntityID | Primary key (clustered) constraint |
| - | AK_Vendor_AccountNumber | AccountNumber | Unique nonclustered index. |