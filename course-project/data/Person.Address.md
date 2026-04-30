# Person.Address

> Street address information for customers, employees, and vendors.

**Documentation:** AdventureWorks
**Schema:** Person
**Name:** Address
**Module:** People

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | AddressID | int | - | Identity | - | Primary key for Address records. |
| - | 2 | - | AddressLine1 | nvarchar(60) | - | - | - | First street address line. |
| - | 3 | - | AddressLine2 | nvarchar(60) | - | - | - | Second street address line. |
| - | 4 | - | City | nvarchar(30) | - | - | - | Name of the city. |
| - | 5 | - | StateProvinceID | int | - | - | Person.StateProvince | Unique identification number for the state or province. Foreign key to StateProvince table. |
| - | 6 | - | PostalCode | nvarchar(15) | - | - | - | Postal code for the street address. |
| - | 7 | - | SpatialLocation | geography | - | - | - | Latitude and longitude of this address. |
| - | 8 | - | rowguid | uniqueidentifier | - | Default: newid() | - | ROWGUIDCOL number uniquely identifying the record. Used to support a merge replication sample. |
| - | 9 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Person.Address | - | Person.StateProvince | Person.Address.StateProvinceID = Person.StateProvince.StateProvinceID | FK_Address_StateProvince_StateProvinceID Foreign key constraint referencing StateProvince.StateProvinceID. |
| Person.BusinessEntityAddress | - | Person.Address | Person.BusinessEntityAddress.AddressID = Person.Address.AddressID | FK_BusinessEntityAddress_Address_AddressID Foreign key constraint referencing Address.AddressID. |
| Sales.SalesOrderHeader | - | Person.Address | Sales.SalesOrderHeader.BillToAddressID = Person.Address.AddressID | FK_SalesOrderHeader_Address_BillToAddressID Foreign key constraint referencing Address.AddressID. |
| Sales.SalesOrderHeader | - | Person.Address | Sales.SalesOrderHeader.ShipToAddressID = Person.Address.AddressID | FK_SalesOrderHeader_Address_ShipToAddressID Foreign key constraint referencing Address.AddressID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_Address_AddressID | AddressID | Primary key (clustered) constraint |
| - | AK_Address_rowguid | rowguid | Unique nonclustered index. Used to support replication samples. |
| - | IX_Address_AddressLine1_AddressLine2_City_StateProvinceID_PostalCode | AddressLine1, AddressLine2, City, StateProvinceID, PostalCode | Nonclustered index. |