# Sales.SalesOrderHeader

> General sales order information.

**Documentation:** AdventureWorks
**Schema:** Sales
**Name:** SalesOrderHeader
**Module:** Sales

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | SalesOrderID | int | - | Identity | - | Primary key. |
| - | 2 | - | RevisionNumber | tinyint | - | Default: 0 | - | Incremental number to track changes to the sales order over time. |
| - | 3 | - | OrderDate | datetime | - | Default: getdate() | - | Dates the sales order was created. |
| - | 4 | - | DueDate | datetime | - | - | - | Date the order is due to the customer. |
| - | 5 | - | ShipDate | datetime | - | - | - | Date the order was shipped to the customer. |
| - | 6 | - | Status | tinyint | - | Default: 1 | - | Order current status. 1 = In process; 2 = Approved; 3 = Backordered; 4 = Rejected; 5 = Shipped; 6 = Cancelled |
| - | 7 | - | OnlineOrderFlag | bit | - | Default: 1 | - | 0 = Order placed by sales person. 1 = Order placed online by customer. |
| - | 8 | - | SalesOrderNumber | nvarchar(25) | - | Computed: isnull(N'SO'+CONVERT([nvarchar](23),[SalesOrderID]),N'*** ERROR ***') | - | Unique sales order identification number. |
| - | 9 | - | PurchaseOrderNumber | nvarchar(25) | - | - | - | Customer purchase order number reference. |
| - | 10 | - | AccountNumber | nvarchar(15) | - | - | - | Financial accounting number reference. |
| - | 11 | - | CustomerID | int | - | - | Sales.Customer | Customer identification number. Foreign key to Customer.BusinessEntityID. |
| - | 12 | - | SalesPersonID | int | - | - | Sales.SalesPerson | Sales person who created the sales order. Foreign key to SalesPerson.BusinessEntityID. |
| - | 13 | - | TerritoryID | int | - | - | Sales.SalesTerritory | Territory in which the sale was made. Foreign key to SalesTerritory.SalesTerritoryID. |
| - | 14 | - | BillToAddressID | int | - | - | Person.Address | Customer billing address. Foreign key to Address.AddressID. |
| - | 15 | - | ShipToAddressID | int | - | - | Person.Address | Customer shipping address. Foreign key to Address.AddressID. |
| - | 16 | - | ShipMethodID | int | - | - | Purchasing.ShipMethod | Shipping method. Foreign key to ShipMethod.ShipMethodID. |
| - | 17 | - | CreditCardID | int | - | - | Sales.CreditCard | Credit card identification number. Foreign key to CreditCard.CreditCardID. |
| - | 18 | - | CreditCardApprovalCode | varchar(15) | - | - | - | Approval code provided by the credit card company. |
| - | 19 | - | CurrencyRateID | int | - | - | Sales.CurrencyRate | Currency exchange rate used. Foreign key to CurrencyRate.CurrencyRateID. |
| - | 20 | - | SubTotal | money | - | Default: 0.00 | - | Sales subtotal. Computed as SUM(SalesOrderDetail.LineTotal)for the appropriate SalesOrderID. |
| - | 21 | - | TaxAmt | money | - | Default: 0.00 | - | Tax amount. |
| - | 22 | - | Freight | money | - | Default: 0.00 | - | Shipping cost. |
| - | 23 | - | TotalDue | money | - | Computed: isnull(([SubTotal]+[TaxAmt])+[Freight],(0)) | - | Total due from customer. Computed as Subtotal + TaxAmt + Freight. |
| - | 24 | - | Comment | nvarchar(128) | - | - | - | Sales representative comments. |
| - | 25 | - | rowguid | uniqueidentifier | - | Default: newid() | - | ROWGUIDCOL number uniquely identifying the record. Used to support a merge replication sample. |
| - | 26 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Sales.SalesOrderHeader | - | Person.Address | Sales.SalesOrderHeader.BillToAddressID = Person.Address.AddressID | FK_SalesOrderHeader_Address_BillToAddressID Foreign key constraint referencing Address.AddressID. |
| Sales.SalesOrderHeader | - | Person.Address | Sales.SalesOrderHeader.ShipToAddressID = Person.Address.AddressID | FK_SalesOrderHeader_Address_ShipToAddressID Foreign key constraint referencing Address.AddressID. |
| Sales.SalesOrderHeader | - | Sales.CreditCard | Sales.SalesOrderHeader.CreditCardID = Sales.CreditCard.CreditCardID | FK_SalesOrderHeader_CreditCard_CreditCardID Foreign key constraint referencing CreditCard.CreditCardID. |
| Sales.SalesOrderHeader | - | Sales.CurrencyRate | Sales.SalesOrderHeader.CurrencyRateID = Sales.CurrencyRate.CurrencyRateID | FK_SalesOrderHeader_CurrencyRate_CurrencyRateID Foreign key constraint referencing CurrencyRate.CurrencyRateID. |
| Sales.SalesOrderHeader | - | Sales.Customer | Sales.SalesOrderHeader.CustomerID = Sales.Customer.CustomerID | FK_SalesOrderHeader_Customer_CustomerID Foreign key constraint referencing Customer.CustomerID. |
| Sales.SalesOrderHeader | - | Sales.SalesPerson | Sales.SalesOrderHeader.SalesPersonID = Sales.SalesPerson.BusinessEntityID | FK_SalesOrderHeader_SalesPerson_SalesPersonID Foreign key constraint referencing SalesPerson.SalesPersonID. |
| Sales.SalesOrderHeader | - | Sales.SalesTerritory | Sales.SalesOrderHeader.TerritoryID = Sales.SalesTerritory.TerritoryID | FK_SalesOrderHeader_SalesTerritory_TerritoryID Foreign key constraint referencing SalesTerritory.TerritoryID. |
| Sales.SalesOrderHeader | - | Purchasing.ShipMethod | Sales.SalesOrderHeader.ShipMethodID = Purchasing.ShipMethod.ShipMethodID | FK_SalesOrderHeader_ShipMethod_ShipMethodID Foreign key constraint referencing ShipMethod.ShipMethodID. |
| Sales.SalesOrderDetail | - | Sales.SalesOrderHeader | Sales.SalesOrderDetail.SalesOrderID = Sales.SalesOrderHeader.SalesOrderID | FK_SalesOrderDetail_SalesOrderHeader_SalesOrderID Foreign key constraint referencing SalesOrderHeader.PurchaseOrderID. |
| Sales.SalesOrderHeaderSalesReason | - | Sales.SalesOrderHeader | Sales.SalesOrderHeaderSalesReason.SalesOrderID = Sales.SalesOrderHeader.SalesOrderID | FK_SalesOrderHeaderSalesReason_SalesOrderHeader_SalesOrderID Foreign key constraint referencing SalesOrderHeader.SalesOrderID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_SalesOrderHeader_SalesOrderID | SalesOrderID | Primary key (clustered) constraint |
| - | AK_SalesOrderHeader_rowguid | rowguid | Unique nonclustered index. Used to support replication samples. |
| - | AK_SalesOrderHeader_SalesOrderNumber | SalesOrderNumber | Unique nonclustered index. |