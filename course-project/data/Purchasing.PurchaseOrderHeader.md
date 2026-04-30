# Purchasing.PurchaseOrderHeader

> General purchase order information. See PurchaseOrderDetail.

**Documentation:** AdventureWorks
**Schema:** Purchasing
**Name:** PurchaseOrderHeader
**Module:** Purchasing

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | PurchaseOrderID | int | - | Identity | - | Primary key. |
| - | 2 | - | RevisionNumber | tinyint | - | Default: 0 | - | Incremental number to track changes to the purchase order over time. |
| - | 3 | - | Status | tinyint | - | Default: 1 | - | Order current status. 1 = Pending; 2 = Approved; 3 = Rejected; 4 = Complete |
| - | 4 | - | EmployeeID | int | - | - | HumanResources.Employee | Employee who created the purchase order. Foreign key to Employee.BusinessEntityID. |
| - | 5 | - | VendorID | int | - | - | Purchasing.Vendor | Vendor with whom the purchase order is placed. Foreign key to Vendor.BusinessEntityID. |
| - | 6 | - | ShipMethodID | int | - | - | Purchasing.ShipMethod | Shipping method. Foreign key to ShipMethod.ShipMethodID. |
| - | 7 | - | OrderDate | datetime | - | Default: getdate() | - | Purchase order creation date. |
| - | 8 | - | ShipDate | datetime | - | - | - | Estimated shipment date from the vendor. |
| - | 9 | - | SubTotal | money | - | Default: 0.00 | - | Purchase order subtotal. Computed as SUM(PurchaseOrderDetail.LineTotal)for the appropriate PurchaseOrderID. |
| - | 10 | - | TaxAmt | money | - | Default: 0.00 | - | Tax amount. |
| - | 11 | - | Freight | money | - | Default: 0.00 | - | Shipping cost. |
| - | 12 | - | TotalDue | money | - | Computed: isnull(([SubTotal]+[TaxAmt])+[Freight],(0)) | - | Total due to vendor. Computed as Subtotal + TaxAmt + Freight. |
| - | 13 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Purchasing.PurchaseOrderHeader | - | HumanResources.Employee | Purchasing.PurchaseOrderHeader.EmployeeID = HumanResources.Employee.BusinessEntityID | FK_PurchaseOrderHeader_Employee_EmployeeID Foreign key constraint referencing Employee.EmployeeID. |
| Purchasing.PurchaseOrderHeader | - | Purchasing.ShipMethod | Purchasing.PurchaseOrderHeader.ShipMethodID = Purchasing.ShipMethod.ShipMethodID | FK_PurchaseOrderHeader_ShipMethod_ShipMethodID Foreign key constraint referencing ShipMethod.ShipMethodID. |
| Purchasing.PurchaseOrderHeader | - | Purchasing.Vendor | Purchasing.PurchaseOrderHeader.VendorID = Purchasing.Vendor.BusinessEntityID | FK_PurchaseOrderHeader_Vendor_VendorID Foreign key constraint referencing Vendor.VendorID. |
| Purchasing.PurchaseOrderDetail | - | Purchasing.PurchaseOrderHeader | Purchasing.PurchaseOrderDetail.PurchaseOrderID = Purchasing.PurchaseOrderHeader.PurchaseOrderID | FK_PurchaseOrderDetail_PurchaseOrderHeader_PurchaseOrderID Foreign key constraint referencing PurchaseOrderHeader.PurchaseOrderID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_PurchaseOrderHeader_PurchaseOrderID | PurchaseOrderID | Primary key (clustered) constraint |