# Person.Person

> Human beings involved with AdventureWorks: employees, customer contacts, and vendor contacts.

**Documentation:** AdventureWorks
**Schema:** Person
**Name:** Person
**Module:** People

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | BusinessEntityID | int | - | - | Person.BusinessEntity | Primary key for Person records. |
| - | 2 | - | PersonType | nchar(2) | - | - | - | Primary type of person: SC = Store Contact, IN = Individual (retail) customer, SP = Sales person, EM = Employee (non-sales), VC = Vendor contact, GC = General contact |
| - | 3 | - | NameStyle | bit | - | Default: 0 | - | 0 = The data in FirstName and LastName are stored in western style (first name, last name) order. 1 = Eastern style (last name, first name) order. |
| - | 4 | - | Title | nvarchar(8) | - | - | - | A courtesy title. For example, Mr. or Ms. |
| - | 5 | - | FirstName | nvarchar(50) | - | - | - | First name of the person. |
| - | 6 | - | MiddleName | nvarchar(50) | - | - | - | Middle name or middle initial of the person. |
| - | 7 | - | LastName | nvarchar(50) | - | - | - | Last name of the person. |
| - | 8 | - | Suffix | nvarchar(10) | - | - | - | Surname suffix. For example, Sr. or Jr. |
| - | 9 | - | EmailPromotion | int | - | Default: 0 | - | 0 = Contact does not wish to receive e-mail promotions, 1 = Contact does wish to receive e-mail promotions from AdventureWorks, 2 = Contact does wish to receive e-mail promotions from AdventureWorks and selected partners. |
| - | 10 | - | AdditionalContactInfo | xml | - | - | - | Additional contact information about the person stored in xml format. |
| - | 11 | - | Demographics | xml | - | - | - | Personal information such as hobbies, and income collected from online shoppers. Used for sales analysis. |
| - | 12 | - | rowguid | uniqueidentifier | - | Default: newid() | - | ROWGUIDCOL number uniquely identifying the record. Used to support a merge replication sample. |
| - | 13 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Person.Person | - | Person.BusinessEntity | Person.Person.BusinessEntityID = Person.BusinessEntity.BusinessEntityID | FK_Person_BusinessEntity_BusinessEntityID Foreign key constraint referencing BusinessEntity.BusinessEntityID. |
| Person.BusinessEntityContact | - | Person.Person | Person.BusinessEntityContact.PersonID = Person.Person.BusinessEntityID | FK_BusinessEntityContact_Person_PersonID Foreign key constraint referencing Person.BusinessEntityID. |
| Sales.Customer | - | Person.Person | Sales.Customer.PersonID = Person.Person.BusinessEntityID | FK_Customer_Person_PersonID Foreign key constraint referencing Person.BusinessEntityID. |
| Person.EmailAddress | - | Person.Person | Person.EmailAddress.BusinessEntityID = Person.Person.BusinessEntityID | FK_EmailAddress_Person_BusinessEntityID Foreign key constraint referencing Person.BusinessEntityID. |
| HumanResources.Employee | - | Person.Person | HumanResources.Employee.BusinessEntityID = Person.Person.BusinessEntityID | FK_Employee_Person_BusinessEntityID Foreign key constraint referencing Person.BusinessEntityID. |
| Person.Password | - | Person.Person | Person.Password.BusinessEntityID = Person.Person.BusinessEntityID | FK_Password_Person_BusinessEntityID Foreign key constraint referencing Person.BusinessEntityID. |
| Sales.PersonCreditCard | - | Person.Person | Sales.PersonCreditCard.BusinessEntityID = Person.Person.BusinessEntityID | FK_PersonCreditCard_Person_BusinessEntityID Foreign key constraint referencing Person.BusinessEntityID. |
| Person.PersonPhone | - | Person.Person | Person.PersonPhone.BusinessEntityID = Person.Person.BusinessEntityID | FK_PersonPhone_Person_BusinessEntityID Foreign key constraint referencing Person.BusinessEntityID. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_Person_BusinessEntityID | BusinessEntityID | Primary key (clustered) constraint |
| - | AK_Person_rowguid | rowguid | Unique nonclustered index. Used to support replication samples. |