# Introduction to DAX Functions

## Executive summary
Data Analysis Expressions (DAX) is the formula language used in Power BI, Analysis Services, and Power Pivot in Excel. DAX provides a rich library of functions and operators to create calculated columns, measures, and tables. This guide gives a practical introduction to DAX functions, core concepts (evaluation contexts), common function categories, examples, performance and best-practice recommendations, and useful learning resources.

---

## 1. What is DAX?
- DAX is a functional language designed for data modeling and analytics on tabular data.
- It combines functions, operators, and values to perform calculations on data in a semantic model.
- Typical uses: measures (dynamic aggregations), calculated columns (row-level calculations stored in the model), calculated tables (tables derived from existing model data).

## 2. Core concepts
- Evaluation contexts:
  - Row context: when a formula is evaluated for each row of a table (e.g., calculated column or inside an iterator like SUMX).
  - Filter context: the set of filters applied to a calculation (visual filters, slicers, CALCULATE, relationships). Measures naturally run in a filter context.
- CALCULATE: central function to modify filter context. Many advanced DAX patterns are built around CALCULATE.
- Variables (VAR / RETURN): improve readability and performance by computing expressions once and reusing the result.

## 3. Function categories (high-level)
- Aggregation functions: SUM, AVERAGE, MIN, MAX, COUNT, DISTINCTCOUNT.
- Iterator functions (end with X): SUMX, AVERAGEX, COUNTX — operate row-by-row and return a scalar by aggregating the evaluated expression.
- Filter and lookup functions: FILTER, ALL, ALLEXCEPT, VALUES, RELATED, RELATEDTABLE.
- Time intelligence: SAMEPERIODLASTYEAR, DATESYTD, DATEADD, TOTALYTD.
- Logical: IF, SWITCH, AND, OR.
- Text: CONCATENATE, CONCATENATEX, LEFT, RIGHT, SEARCH.
- Math and trig: ROUND, INT, ABS, MOD.
- Table manipulation: ADDCOLUMNS, SUMMARIZE, NATURALINNERJOIN, CROSSJOIN.
- Statistical: STDEV.P, STDEV.S, RANKX.
- Information/metadata: ISBLANK, ISERROR, ISNUMBER.

## 4. Typical patterns and examples
Note: Examples use common DAX syntax for measures.

- Simple aggregation (measure):
  Total Sales = SUM(Sales[SalesAmount])

- Using CALCULATE to change filters:
  Sales Last Year =
    CALCULATE([Total Sales], SAMEPERIODLASTYEAR(Calendar[Date]))

- Iterator example (row-by-row):
  Total Profit = SUMX(Sales, Sales[Quantity] * Sales[UnitPrice] - Sales[Quantity] * Sales[UnitCost])
  Use SUMX when you need row-level arithmetic before aggregating.

- Filter + iterator: compute sales for a product subset:
  Sales of Flagged Products =
    CALCULATE(
      [Total Sales],
      FILTER(Products, Products[IsFlagged] = TRUE())
    )

- Using variables for clarity and performance:
  Avg Price per Transaction =
    VAR TransCount = DISTINCTCOUNT(Sales[TransactionID])
    VAR Total = SUM(Sales[SalesAmount])
    RETURN
      DIVIDE(Total, TransCount)

- Concatenation across rows:
  Product List = CONCATENATEX(VALUES(Products[ProductName]), Products[ProductName], ", ")

- Ranking with RANKX:
  Product Rank by Sales =
    RANKX(ALL(Products), [Total Sales])

## 5. Time intelligence essentials
- Use a contiguous date table marked as a Date table in the model — many time intelligence functions require it.
- Common time functions: DATESYTD, TOTALYTD, SAMEPERIODLASTYEAR, DATEADD, PREVIOUSMONTH, PARALLELPERIOD.
- Example: Year-to-date sales
  YTD Sales = TOTALYTD([Total Sales], Calendar[Date])

## 6. Performance tips and best practices
- Prefer measures over calculated columns for aggregations and metrics — measures calculate on demand in the current filter context and usually save memory.
- Minimize row-by-row operations on large tables. Where possible, push aggregation to column-level functions (SUM, COUNT) instead of iterators.
- Use variables (VAR) to avoid repeated calculations and improve readability.
- Keep FILTER and complex table expressions as selective as possible; FILTER iterates over a table and can be costly.
- When using CALCULATE, be explicit about which filters you change. Use ALL/ALLEXCEPT/ALLSELECTED carefully to avoid removing required filters.
- Use SUMX on a smaller table (e.g., a summarized table) if you only need aggregated results per group.
- Avoid excessive nested iterators and deeply nested CALCULATE calls.

## 7. Debugging and validating DAX
- Use tools and techniques:
  - DAX Studio: run queries, inspect query plans, check server timings.
  - Evaluate intermediate results by creating temporary measures using VAR and RETURN.
  - Use EVALUATE and ROW in DAX Studio to preview tables and expressions.

## 8. Common pitfalls
- Confusing row context and filter context — remember a CALCULATE converts row context to filter context.
- Not having a proper date table — time intelligence functions may return incorrect results.
- Using EARLIER without understanding nested row contexts — variables are often a better modern alternative.
- Relying on implicit relationships when a model lacks explicit foreign keys — use RELATED/RELATEDTABLE with care.

## 9. Learning resources
- Official Microsoft DAX documentation and function reference: https://learn.microsoft.com/en-us/dax/dax-function-reference
- DAX overview: https://learn.microsoft.com/en-us/dax/
- DAX Guide (community-driven reference): https://dax.guide/
- Tutorials and performance tips: DAX patterns and SQLBI articles (search SQLBI site for specific patterns)

---

## Sources
- https://learn.microsoft.com/en-us/dax/dax-function-reference
- https://learn.microsoft.com/en-us/dax/
- https://dax.guide/
