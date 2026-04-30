# Production.BillOfMaterials

> Items required to make bicycles and bicycle subassemblies. It identifies the heirarchical relationship between a parent product and its components.

**Documentation:** AdventureWorks
**Schema:** Production
**Name:** BillOfMaterials
**Module:** Manufacturing

---

## Columns
|  |  | Key | Name | Data type | Null | Attributes | References | Description |
|---|---|---|---|---|---|---|---|---|
| - | 1 | - | BillOfMaterialsID | int | - | Identity | - | Primary key for BillOfMaterials records. |
| - | 2 | - | ProductAssemblyID | int | - | - | Production.Product | Parent product identification number. Foreign key to Product.ProductID. |
| - | 3 | - | ComponentID | int | - | - | Production.Product | Component identification number. Foreign key to Product.ProductID. |
| - | 4 | - | StartDate | datetime | - | Default: getdate() | - | Date the component started being used in the assembly item. |
| - | 5 | - | EndDate | datetime | - | - | - | Date the component stopped being used in the assembly item. |
| - | 6 | - | UnitMeasureCode | nchar(3) | - | - | Production.UnitMeasure | Standard code identifying the unit of measure for the quantity. |
| - | 7 | - | BOMLevel | smallint | - | - | - | Indicates the depth the component is from its parent (AssemblyID). |
| - | 8 | - | PerAssemblyQty | decimal(8, 2) | - | Default: 1.00 | - | Quantity of the component needed to create the assembly. |
| - | 9 | - | ModifiedDate | datetime | - | Default: getdate() | - | Date and time the record was last updated. |

## Relations
| Foreign table |  | Primary table | Join | Title / Name / Description |
|---|---|---|---|---|
| Production.BillOfMaterials | - | Production.Product | Production.BillOfMaterials.ComponentID = Production.Product.ProductID | FK_BillOfMaterials_Product_ComponentID Foreign key constraint referencing Product.ProductAssemblyID. |
| Production.BillOfMaterials | - | Production.Product | Production.BillOfMaterials.ProductAssemblyID = Production.Product.ProductID | FK_BillOfMaterials_Product_ProductAssemblyID Foreign key constraint referencing Product.ProductAssemblyID. |
| Production.BillOfMaterials | - | Production.UnitMeasure | Production.BillOfMaterials.UnitMeasureCode = Production.UnitMeasure.UnitMeasureCode | FK_BillOfMaterials_UnitMeasure_UnitMeasureCode Foreign key constraint referencing UnitMeasure.UnitMeasureCode. |

## Unique Keys
|  | Key name | Columns | Description |
|---|---|---|---|
| - | PK_BillOfMaterials_BillOfMaterialsID | BillOfMaterialsID | Primary key (clustered) constraint |
| - | AK_BillOfMaterials_ProductAssemblyID_ComponentID_StartDate | ProductAssemblyID, ComponentID, StartDate | Clustered index. |