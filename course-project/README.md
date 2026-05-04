### Опис тулів для агентів:
|Назва|Параметри|Опис|
|--|--|--|
|`web_search`|`query: str`|Шукає актуальну інформацію в інтернеті через DuckDuckGo. Повертає перелік знайдених посилань з даними про заголовок, URL, фрагмент тексту. Використовується як перший крок пошуку.|
|`read_url`|`url: str`|Отримує основний текст із вебсторінки (або PDF, якщо це пряме посилання на pdf-звіт чи статтю).|
|`knowledge_search`|`query: str`|Пошук у локальній базі знань за допомогою гібридного пошуку (hybrid retrieval) та реранкінгу.|
|`execute_sql_query`|`query: str`|Виконання sql запиту з обмеженням на timeout та вісутність заборонених операторів.|
|`get_table_structure`|`table_name: str, schema_name: str`|Повертає структуру вказаної таблиці (назви полів + типи даних).|
|`ask_user_for_clarification`|`question: str`|Комунікація з користувачем (запитання / уточнення).|
|`list_schemas_and_tables`|`-`|Повертає повний перелік таблиць (назва+схема).|
|`get_sample_rows`|`table_name: str, schema_name: str`|Повертає топ-5 записів з вказаної таблиці для "знайомства" з даними.|
|`get_view_definition`|`view_name: str, schema_name: str`|Повертає визначення представлення (view).|
|`get_sql_execution_plan`|`sql_query: str`|Повертає оціночний план запиту|

#### Результат для `deepeval test run tests/test_e2e.py`:

```
-------------------------------------------------- Captured log call --------------------------------------------------
INFO     deepeval.evaluate.execute:execute.py:779 in _a_execute_llm_test_cases
================================================ slowest 10 durations =================================================
93.89s call     tests/test_e2e.py::test_e2e_high_reach_products
68.49s call     tests/test_e2e.py::test_e2e_recent_hires
66.04s call     tests/test_e2e.py::test_e2e_yoy_revenue_growth
43.31s call     tests/test_e2e.py::test_e2e_email_domain_distribution
40.37s call     tests/test_e2e.py::test_e2e_aw_customers_without_orders
0.01s teardown tests/test_e2e.py::test_e2e_yoy_revenue_growth

(4 durations < 0.005s hidden.  Use -vv to show these durations.)
=============================================== short test summary info ===============================================
FAILED tests/test_e2e.py::test_e2e_aw_customers_without_orders - AssertionError: Metrics: Task Accuracy and Completion [GEval] (score: 0.7, threshold: 0.8, strict: False, error: No...
FAILED tests/test_e2e.py::test_e2e_high_reach_products - AssertionError: Metrics: Production SQL Quality [GEval] (score: 0.6, threshold: 0.8, strict: False, error: None, re...
2 failed, 3 passed, 4 warnings in 382.70s (0:06:22)
                                                      Test Results
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┓
┃ Test case                  ┃ Metric                     ┃ Score                      ┃ Status ┃ Overall Success Rate ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━┩
│ test_e2e_recent_hires      │                            │                            │        │ 100.0%               │
│                            │ Task Accuracy and          │ 0.9 (threshold=0.8,        │ PASSED │                      │
│                            │ Completion [GEval]         │ evaluation                 │        │                      │
│                            │                            │ model=gpt-5.4-mini,        │        │                      │
│                            │                            │ reason=The response        │        │                      │
│                            │                            │ matches the requirements   │        │                      │
│                            │                            │ well: it joins Employee,   │        │                      │
│                            │                            │ EmployeeDepartmentHistory, │        │                      │
│                            │                            │ Department, and            │        │                      │
│                            │                            │ Person.Person; filters     │        │                      │
│                            │                            │ current assignments with   │        │                      │
│                            │                            │ EndDate IS NULL; uses      │        │                      │
│                            │                            │ ROW_NUMBER() partitioned   │        │                      │
│                            │                            │ by department and ordered  │        │                      │
│                            │                            │ by HireDate DESC; and      │        │                      │
│                            │                            │ returns the required       │        │                      │
│                            │                            │ DepartmentName, FirstName, │        │                      │
│                            │                            │ LastName, and HireDate     │        │                      │
│                            │                            │ columns. The only minor    │        │                      │
│                            │                            │ issue is that it includes  │        │                      │
│                            │                            │ extra non-code description │        │                      │
│                            │                            │ text, but the SQL itself   │        │                      │
│                            │                            │ satisfies the task.,       │        │                      │
│                            │                            │ error=None)                │        │                      │
│                            │ Production SQL Quality     │ 0.8 (threshold=0.8,        │ PASSED │                      │
│                            │ [GEval]                    │ evaluation                 │        │                      │
│                            │                            │ model=gpt-5.4-mini,        │        │                      │
│                            │                            │ reason=The query is        │        │                      │
│                            │                            │ syntactically valid T-SQL, │        │                      │
│                            │                            │ uses the required tables,  │        │                      │
│                            │                            │ filters                    │        │                      │
│                            │                            │ EmployeeDepartmentHistory  │        │                      │
│                            │                            │ with EndDate IS NULL, and  │        │                      │
│                            │                            │ applies ROW_NUMBER()       │        │                      │
│                            │                            │ partitioned by department  │        │                      │
│                            │                            │ with HireDate DESC. It is  │        │                      │
│                            │                            │ also well formatted and    │        │                      │
│                            │                            │ includes helpful inline    │        │                      │
│                            │                            │ comments. However, it does │        │                      │
│                            │                            │ not show production-level  │        │                      │
│                            │                            │ defensive programming      │        │                      │
│                            │                            │ beyond a simple            │        │                      │
│                            │                            │ tie-breaker, and the       │        │                      │
│                            │                            │ submission includes no     │        │                      │
│                            │                            │ evidence of placeholder    │        │                      │
│                            │                            │ schema names or            │        │                      │
│                            │                            │ schema-tool validation     │        │                      │
│                            │                            │ being an issue, so only    │        │                      │
│                            │                            │ the core SQL quality and   │        │                      │
│                            │                            │ requirements are clearly   │        │                      │
│                            │                            │ satisfied., error=None)    │        │                      │
│                            │ Query Efficiency [GEval]   │ 1.0 (threshold=0.8,        │ PASSED │                      │
│                            │                            │ evaluation                 │        │                      │
│                            │                            │ model=gpt-5.4-mini,        │        │                      │
│                            │                            │ reason=The query meets the │        │                      │
│                            │                            │ requirements well: it      │        │                      │
│                            │                            │ explicitly selects         │        │                      │
│                            │                            │ DepartmentName, FirstName, │        │                      │
│                            │                            │ LastName, and HireDate     │        │                      │
│                            │                            │ instead of using SELECT *, │        │                      │
│                            │                            │ joins the required tables, │        │                      │
│                            │                            │ filters                    │        │                      │
│                            │                            │ EmployeeDepartmentHistory  │        │                      │
│                            │                            │ with EndDate IS NULL, and  │        │                      │
│                            │                            │ uses ROW_NUMBER()          │        │                      │
│                            │                            │ partitioned by department  │        │                      │
│                            │                            │ with HireDate DESC to find │        │                      │
│                            │                            │ the newest active          │        │                      │
│                            │                            │ employee. It also avoids   │        │                      │
│                            │                            │ correlated subqueries and  │        │                      │
│                            │                            │ does not use inefficient   │        │                      │
│                            │                            │ aggregation, though the    │        │                      │
│                            │                            │ final ORDER BY is          │        │                      │
│                            │                            │ unnecessary for the core   │        │                      │
│                            │                            │ logic., error=None)        │        │                      │
│                            │ Security and Safety        │ 1.0 (threshold=1.0,        │ PASSED │                      │
│                            │ [GEval]                    │ evaluation                 │        │                      │
│                            │                            │ model=gpt-5.4-mini,        │        │                      │
│                            │                            │ reason=The output is a     │        │                      │
│                            │                            │ read-only SELECT query     │        │                      │
│                            │                            │ with a CTE and no INSERT,  │        │                      │
│                            │                            │ UPDATE, DELETE, TRUNCATE,  │        │                      │
│                            │                            │ DROP, ALTER, CREATE, or    │        │                      │
│                            │                            │ dynamic SQL. It also       │        │                      │
│                            │                            │ matches the task           │        │                      │
│                            │                            │ requirements by joining    │        │                      │
│                            │                            │ the four required tables,  │        │                      │
│                            │                            │ filtering                  │        │                      │
│                            │                            │ EmployeeDepartmentHistory  │        │                      │
│                            │                            │ with EndDate IS NULL, and  │        │                      │
│                            │                            │ using ROW_NUMBER           │        │                      │
│                            │                            │ partitioned by             │        │                      │
│                            │                            │ DepartmentID ordered by    │        │                      │
│                            │                            │ HireDate DESC to return    │        │                      │
│                            │                            │ DepartmentName, FirstName, │        │                      │
│                            │                            │ LastName, and HireDate.,   │        │                      │
│                            │                            │ error=None)                │        │                      │
│                            │ Schema Hallucination Free  │ 0.9 (threshold=0.9,        │ PASSED │                      │
│                            │ [GEval]                    │ evaluation                 │        │                      │
│                            │                            │ model=gpt-5.4-mini,        │        │                      │
│                            │                            │ reason=The SQL matches the │        │                      │
│                            │                            │ stated requirements well:  │        │                      │
│                            │                            │ it joins                   │        │                      │
│                            │                            │ HumanResources.Employee,   │        │                      │
│                            │                            │ HumanResources.EmployeeDe… │        │                      │
│                            │                            │ HumanResources.Department, │        │                      │
│                            │                            │ and Person.Person; filters │        │                      │
│                            │                            │ EmployeeDepartmentHistory  │        │                      │
│                            │                            │ with EndDate IS NULL;      │        │                      │
│                            │                            │ returns DepartmentName,    │        │                      │
│                            │                            │ FirstName, LastName, and   │        │                      │
│                            │                            │ HireDate; and uses         │        │                      │
│                            │                            │ ROW_NUMBER partitioned by  │        │                      │
│                            │                            │ department with HireDate   │        │                      │
│                            │                            │ DESC. No invented          │        │                      │
│                            │                            │ placeholder tables or      │        │                      │
│                            │                            │ columns appear. The only   │        │                      │
│                            │                            │ minor deviation is the     │        │                      │
│                            │                            │ extra BusinessEntityID     │        │                      │
│                            │                            │ tie-breaker and ordering   │        │                      │
│                            │                            │ in the final output, which │        │                      │
│                            │                            │ do not conflict with the   │        │                      │
│                            │                            │ prompt., error=None)       │        │                      │
│                            │ Maintainability [GEval]    │ 0.9 (threshold=0.7,        │ PASSED │                      │
│                            │                            │ evaluation                 │        │                      │
│                            │                            │ model=gpt-5.4-mini,        │        │                      │
│                            │                            │ reason=The query uses      │        │                      │
│                            │                            │ clear aliases for all      │        │                      │
│                            │                            │ joined tables (edh, e, d,  │        │                      │
│                            │                            │ p), includes explicit      │        │                      │
│                            │                            │ aliases for calculated     │        │                      │
│                            │                            │ columns like               │        │                      │
│                            │                            │ DepartmentName and rn, and │        │                      │
│                            │                            │ is cleanly indented with   │        │                      │
│                            │                            │ logical                    │        │                      │
│                            │                            │ CTE/SELECT/FROM/WHERE      │        │                      │
│                            │                            │ structure. The description │        │                      │
│                            │                            │ accurately explains the    │        │                      │
│                            │                            │ intent, including          │        │                      │
│                            │                            │ filtering EndDate IS NULL  │        │                      │
│                            │                            │ and using ROW_NUMBER() to  │        │                      │
│                            │                            │ pick the newest active     │        │                      │
│                            │                            │ employee per department.   │        │                      │
│                            │                            │ Minor deduction because    │        │                      │
│                            │                            │ the result uses a          │        │                      │
│                            │                            │ tie-breaker on             │        │                      │
│                            │                            │ BusinessEntityID, but that │        │                      │
│                            │                            │ does not conflict with the │        │                      │
│                            │                            │ requirements., error=None) │        │                      │
│                            │                            │                            │        │                      │
│ test_e2e_aw_customers_wit… │                            │                            │        │ 66.67%               │
│                            │ Task Accuracy and          │ 0.7 (threshold=0.8,        │ FAILED │                      │
│                            │ Completion [GEval]         │ evaluation                 │        │                      │
│                            │                            │ model=gpt-5.4-mini,        │        │                      │
│                            │                            │ reason=The SQL correctly   │        │                      │
│                            │                            │ identifies customers       │        │                      │
│                            │                            │ without orders using a     │        │                      │
│                            │                            │ LEFT JOIN and NULL filter  │        │                      │
│                            │                            │ against Sales.Customer and │        │                      │
│                            │                            │ Sales.SalesOrderHeader,    │        │                      │
│                            │                            │ matching the requested     │        │                      │
│                            │                            │ anti-join logic. However,  │        │                      │
│                            │                            │ the actual output includes │        │                      │
│                            │                            │ extra fields and           │        │                      │
│                            │                            │ explanatory text           │        │                      │
│                            │                            │ ('description' and         │        │                      │
│                            │                            │ comments) instead of only  │        │                      │
│                            │                            │ the final SQL code, which  │        │                      │
│                            │                            │ violates the requirement   │        │                      │
│                            │                            │ to return just the         │        │                      │
│                            │                            │ requested output. It does  │        │                      │
│                            │                            │ return the correct single  │        │                      │
│                            │                            │ column CustomerID and      │        │                      │
│                            │                            │ excludes ordered           │        │                      │
│                            │                            │ customers., error=None)    │        │                      │
│                            │ Production SQL Quality     │ 0.7 (threshold=0.8,        │ FAILED │                      │
│                            │ [GEval]                    │ evaluation                 │        │                      │
│                            │                            │ model=gpt-5.4-mini,        │        │                      │
│                            │                            │ reason=The SQL is          │        │                      │
│                            │                            │ syntactically valid T-SQL  │        │                      │
│                            │                            │ and correctly uses a LEFT  │        │                      │
│                            │                            │ JOIN with a NULL check     │        │                      │
│                            │                            │ against Sales.Customer and │        │                      │
│                            │                            │ Sales.SalesOrderHeader to  │        │                      │
│                            │                            │ find customers with no     │        │                      │
│                            │                            │ orders. It also returns    │        │                      │
│                            │                            │ only CustomerID as         │        │                      │
│                            │                            │ required and includes an   │        │                      │
│                            │                            │ inline comment. However,   │        │                      │
│                            │                            │ it lacks broader           │        │                      │
│                            │                            │ production-level defensive │        │                      │
│                            │                            │ programming, and the       │        │                      │
│                            │                            │ formatting/comments are    │        │                      │
│                            │                            │ minimal rather than        │        │                      │
│                            │                            │ strongly explanatory.      │        │                      │
│                            │                            │ There are no placeholder   │        │                      │
│                            │                            │ schema names, so schema    │        │                      │
│                            │                            │ usage appears correct.,    │        │                      │
│                            │                            │ error=None)                │        │                      │
│                            │ Query Efficiency [GEval]   │ 0.8 (threshold=0.8,        │ PASSED │                      │
│                            │                            │ evaluation                 │        │                      │
│                            │                            │ model=gpt-5.4-mini,        │        │                      │
│                            │                            │ reason=The query uses the  │        │                      │
│                            │                            │ required LEFT JOIN with a  │        │                      │
│                            │                            │ NULL check to find         │        │                      │
│                            │                            │ customers without orders,  │        │                      │
│                            │                            │ and it selects the         │        │                      │
│                            │                            │ necessary column           │        │                      │
│                            │                            │ explicitly as CustomerID.  │        │                      │
│                            │                            │ It also avoids correlated  │        │                      │
│                            │                            │ subqueries. However, it    │        │                      │
│                            │                            │ adds DISTINCT redundantly  │        │                      │
│                            │                            │ since the anti-join        │        │                      │
│                            │                            │ already returns one row    │        │                      │
│                            │                            │ per customer, so the       │        │                      │
│                            │                            │ aggregation/duplication    │        │                      │
│                            │                            │ handling is not fully      │        │                      │
│                            │                            │ efficient., error=None)    │        │                      │
│                            │ Security and Safety        │ 1.0 (threshold=1.0,        │ PASSED │                      │
│                            │ [GEval]                    │ evaluation                 │        │                      │
│                            │                            │ model=gpt-5.4-mini,        │        │                      │
│                            │                            │ reason=The output is a     │        │                      │
│                            │                            │ read-only SELECT query     │        │                      │
│                            │                            │ only, with no              │        │                      │
│                            │                            │ INSERT/UPDATE/DELETE/TRUN… │        │                      │
│                            │                            │ no DDL, and no dynamic     │        │                      │
│                            │                            │ SQL. It also matches the   │        │                      │
│                            │                            │ task requirements by using │        │                      │
│                            │                            │ a LEFT JOIN with a NULL    │        │                      │
│                            │                            │ check against              │        │                      │
│                            │                            │ Sales.Customer and         │        │                      │
│                            │                            │ Sales.SalesOrderHeader,    │        │                      │
│                            │                            │ returning CustomerID to    │        │                      │
│                            │                            │ identify customers without │        │                      │
│                            │                            │ orders. One minor issue is │        │                      │
│                            │                            │ the use of DISTINCT, but   │        │                      │
│                            │                            │ it does not violate the    │        │                      │
│                            │                            │ acceptance criteria.,      │        │                      │
│                            │                            │ error=None)                │        │                      │
│                            │ Schema Hallucination Free  │ 1.0 (threshold=0.9,        │ PASSED │                      │
│                            │ [GEval]                    │ evaluation                 │        │                      │
│                            │                            │ model=gpt-5.4-mini,        │        │                      │
│                            │                            │ reason=The SQL uses the    │        │                      │
│                            │                            │ specified tables,          │        │                      │
│                            │                            │ Sales.Customer and         │        │                      │
│                            │                            │ Sales.SalesOrderHeader,    │        │                      │
│                            │                            │ and correctly applies a    │        │                      │
│                            │                            │ LEFT JOIN with a NULL      │        │                      │
│                            │                            │ check to find customers    │        │                      │
│                            │                            │ with no orders. It also    │        │                      │
│                            │                            │ returns only CustomerID,   │        │                      │
│                            │                            │ matching the acceptance    │        │                      │
│                            │                            │ criteria. The use of       │        │                      │
│                            │                            │ DISTINCT is unnecessary    │        │                      │
│                            │                            │ but not harmful, and there │        │                      │
│                            │                            │ are no invented tables or  │        │                      │
│                            │                            │ placeholder columns.,      │        │                      │
│                            │                            │ error=None)                │        │                      │
│                            │ Maintainability [GEval]    │ 0.8 (threshold=0.7,        │ PASSED │                      │
│                            │                            │ evaluation                 │        │                      │
│                            │                            │ model=gpt-5.4-mini,        │        │                      │
│                            │                            │ reason=The query uses      │        │                      │
│                            │                            │ clear aliases for both     │        │                      │
│                            │                            │ joined tables (`c` and     │        │                      │
│                            │                            │ `soh`), is cleanly         │        │                      │
│                            │                            │ indented, and the          │        │                      │
│                            │                            │ description accurately     │        │                      │
│                            │                            │ explains the anti-join     │        │                      │
│                            │                            │ logic for finding          │        │                      │
│                            │                            │ customers with no orders.  │        │                      │
│                            │                            │ However, it includes       │        │                      │
│                            │                            │ `DISTINCT`, which is       │        │                      │
│                            │                            │ unnecessary for a unique   │        │                      │
│                            │                            │ `CustomerID` result and    │        │                      │
│                            │                            │ does not fully address the │        │                      │
│                            │                            │ acceptance criterion that  │        │                      │
│                            │                            │ exactly one column be      │        │                      │
│                            │                            │ returned as a simple       │        │                      │
│                            │                            │ `CustomerID` output,       │        │                      │
│                            │                            │ though the selected column │        │                      │
│                            │                            │ is correct. There are no   │        │                      │
│                            │                            │ calculated columns needing │        │                      │
│                            │                            │ aliases., error=None)      │        │                      │
│                            │                            │                            │        │                      │
│ test_e2e_high_reach_produ… │                            │                            │        │ 83.33%               │
│                            │ Task Accuracy and          │ 0.9 (threshold=0.8,        │ PASSED │                      │
│                            │ Completion [GEval]         │ evaluation                 │        │                      │
│                            │                            │ model=gpt-5.4-mini,        │        │                      │
│                            │                            │ reason=The SQL matches the │        │                      │
│                            │                            │ requested joins and        │        │                      │
│                            │                            │ returns the required       │        │                      │
│                            │                            │ fields ProductName,        │        │                      │
│                            │                            │ UniqueCustomerCount, and   │        │                      │
│                            │                            │ TotalLifetimeRevenue. It   │        │                      │
│                            │                            │ correctly uses             │        │                      │
│                            │                            │ COUNT(DISTINCT             │        │                      │
│                            │                            │ h.CustomerID) and a HAVING │        │                      │
│                            │                            │ clause to keep products    │        │                      │
│                            │                            │ with at least 50 unique    │        │                      │
│                            │                            │ customers. The only minor  │        │                      │
│                            │                            │ issue is that it adds an   │        │                      │
│                            │                            │ ORDER BY not requested,    │        │                      │
│                            │                            │ but that does not affect   │        │                      │
│                            │                            │ correctness., error=None)  │        │                      │
│                            │ Production SQL Quality     │ 0.6 (threshold=0.8,        │ FAILED │                      │
│                            │ [GEval]                    │ evaluation                 │        │                      │
│                            │                            │ model=gpt-5.4-mini,        │        │                      │
│                            │                            │ reason=The SQL is          │        │                      │
│                            │                            │ syntactically valid T-SQL  │        │                      │
│                            │                            │ and correctly joins        │        │                      │
│                            │                            │ Production.Product,        │        │                      │
│                            │                            │ Sales.SalesOrderDetail,    │        │                      │
│                            │                            │ and                        │        │                      │
│                            │                            │ Sales.SalesOrderHeader,    │        │                      │
│                            │                            │ using COUNT(DISTINCT       │        │                      │
│                            │                            │ h.CustomerID) and a HAVING │        │                      │
│                            │                            │ clause for the 50-customer │        │                      │
│                            │                            │ threshold. However, it     │        │                      │
│                            │                            │ lacks production-level     │        │                      │
│                            │                            │ defensive programming and  │        │                      │
│                            │                            │ does not include any       │        │                      │
│                            │                            │ inline comments. It also   │        │                      │
│                            │                            │ does not demonstrate any   │        │                      │
│                            │                            │ schema-tool issue, and     │        │                      │
│                            │                            │ there are no placeholder   │        │                      │
│                            │                            │ schema names present.,     │        │                      │
│                            │                            │ error=None)                │        │                      │
│                            │ Query Efficiency [GEval]   │ 0.9 (threshold=0.8,        │ PASSED │                      │
│                            │                            │ evaluation                 │        │                      │
│                            │                            │ model=gpt-5.4-mini,        │        │                      │
│                            │                            │ reason=The query meets the │        │                      │
│                            │                            │ key requirements well: it  │        │                      │
│                            │                            │ explicitly selects only    │        │                      │
│                            │                            │ the needed columns, uses   │        │                      │
│                            │                            │ joins across the required  │        │                      │
│                            │                            │ tables, applies            │        │                      │
│                            │                            │ COUNT(DISTINCT             │        │                      │
│                            │                            │ h.CustomerID) with a       │        │                      │
│                            │                            │ HAVING clause for the      │        │                      │
│                            │                            │ 50-customer threshold, and │        │                      │
│                            │                            │ avoids correlated          │        │                      │
│                            │                            │ subqueries. It also uses   │        │                      │
│                            │                            │ efficient aggregation at   │        │                      │
│                            │                            │ the product level without  │        │                      │
│                            │                            │ redundant grouping. One    │        │                      │
│                            │                            │ minor gap is that it       │        │                      │
│                            │                            │ groups by p.Name instead   │        │                      │
│                            │                            │ of a stable product key,   │        │                      │
│                            │                            │ which could merge products │        │                      │
│                            │                            │ with duplicate names, but  │        │                      │
│                            │                            │ overall it aligns strongly │        │                      │
│                            │                            │ with the evaluation        │        │                      │
│                            │                            │ steps., error=None)        │        │                      │
│                            │ Security and Safety        │ 1.0 (threshold=1.0,        │ PASSED │                      │
│                            │ [GEval]                    │ evaluation                 │        │                      │
│                            │                            │ model=gpt-5.4-mini,        │        │                      │
│                            │                            │ reason=The output contains │        │                      │
│                            │                            │ a single read-only SELECT  │        │                      │
│                            │                            │ query with no INSERT,      │        │                      │
│                            │                            │ UPDATE, DELETE, TRUNCATE,  │        │                      │
│                            │                            │ DROP, ALTER, CREATE, or    │        │                      │
│                            │                            │ dynamic SQL. It also       │        │                      │
│                            │                            │ matches the task           │        │                      │
│                            │                            │ requirements by joining    │        │                      │
│                            │                            │ Production.Product,        │        │                      │
│                            │                            │ Sales.SalesOrderDetail,    │        │                      │
│                            │                            │ and                        │        │                      │
│                            │                            │ Sales.SalesOrderHeader,    │        │                      │
│                            │                            │ using COUNT(DISTINCT       │        │                      │
│                            │                            │ h.CustomerID), and         │        │                      │
│                            │                            │ applying a HAVING clause   │        │                      │
│                            │                            │ for at least 50 unique     │        │                      │
│                            │                            │ customers., error=None)    │        │                      │
│                            │ Schema Hallucination Free  │ 1.0 (threshold=0.9,        │ PASSED │                      │
│                            │ [GEval]                    │ evaluation                 │        │                      │
│                            │                            │ model=gpt-5.4-mini,        │        │                      │
│                            │                            │ reason=The SQL uses        │        │                      │
│                            │                            │ exactly the required       │        │                      │
│                            │                            │ tables:                    │        │                      │
│                            │                            │ Production.Product,        │        │                      │
│                            │                            │ Sales.SalesOrderDetail,    │        │                      │
│                            │                            │ and                        │        │                      │
│                            │                            │ Sales.SalesOrderHeader,    │        │                      │
│                            │                            │ and the columns align with │        │                      │
│                            │                            │ the task by returning      │        │                      │
│                            │                            │ ProductName,               │        │                      │
│                            │                            │ UniqueCustomerCount, and   │        │                      │
│                            │                            │ TotalLifetimeRevenue. It   │        │                      │
│                            │                            │ correctly applies          │        │                      │
│                            │                            │ COUNT(DISTINCT             │        │                      │
│                            │                            │ h.CustomerID) and a HAVING │        │                      │
│                            │                            │ clause to filter products  │        │                      │
│                            │                            │ with at least 50 unique    │        │                      │
│                            │                            │ customers. No invented or  │        │                      │
│                            │                            │ generic placeholder        │        │                      │
│                            │                            │ tables/columns are         │        │                      │
│                            │                            │ present; the only minor    │        │                      │
│                            │                            │ issue is that it orders    │        │                      │
│                            │                            │ the results, which was not │        │                      │
│                            │                            │ requested, but this does   │        │                      │
│                            │                            │ not violate the            │        │                      │
│                            │                            │ requirements., error=None) │        │                      │
│                            │ Maintainability [GEval]    │ 0.9 (threshold=0.7,        │ PASSED │                      │
│                            │                            │ evaluation                 │        │                      │
│                            │                            │ model=gpt-5.4-mini,        │        │                      │
│                            │                            │ reason=The query is well   │        │                      │
│                            │                            │ structured with clear      │        │                      │
│                            │                            │ aliases for all joined     │        │                      │
│                            │                            │ tables (p, d, h), uses     │        │                      │
│                            │                            │ explicit AS aliases for    │        │                      │
│                            │                            │ the calculated columns,    │        │                      │
│                            │                            │ and has clean indentation  │        │                      │
│                            │                            │ across SELECT, FROM, JOIN, │        │                      │
│                            │                            │ GROUP BY, and HAVING. The  │        │                      │
│                            │                            │ description also           │        │                      │
│                            │                            │ accurately explains the    │        │                      │
│                            │                            │ joins, COUNT(DISTINCT      │        │                      │
│                            │                            │ h.CustomerID),             │        │                      │
│                            │                            │ SUM(d.LineTotal), and the  │        │                      │
│                            │                            │ 50-customer HAVING filter. │        │                      │
│                            │                            │ Minor shortcoming: the     │        │                      │
│                            │                            │ requirement says to return │        │                      │
│                            │                            │ ProductName,               │        │                      │
│                            │                            │ UniqueCustomerCount, and   │        │                      │
│                            │                            │ TotalLifetimeRevenue, and  │        │                      │
│                            │                            │ the query provides that,   │        │                      │
│                            │                            │ though it orders the       │        │                      │
│                            │                            │ results additionally,      │        │                      │
│                            │                            │ which is acceptable.,      │        │                      │
│                            │                            │ error=None)                │        │                      │
│                            │                            │                            │        │                      │
│ test_e2e_yoy_revenue_grow… │                            │                            │        │ 100.0%               │
│                            │ Task Accuracy and          │ 1.0 (threshold=0.8,        │ PASSED │                      │
│                            │ Completion [GEval]         │ evaluation                 │        │                      │
│                            │                            │ model=gpt-5.4-mini,        │        │                      │
│                            │                            │ reason=The SQL fully       │        │                      │
│                            │                            │ addresses the request: it  │        │                      │
│                            │                            │ uses                       │        │                      │
│                            │                            │ Sales.SalesOrderHeader and │        │                      │
│                            │                            │ Sales.SalesTerritory,      │        │                      │
│                            │                            │ includes a CTE for annual  │        │                      │
│                            │                            │ territory revenue, applies │        │                      │
│                            │                            │ LAG() by territory and     │        │                      │
│                            │                            │ year, and returns the      │        │                      │
│                            │                            │ required columns           │        │                      │
│                            │                            │ TerritoryName, SalesYear,  │        │                      │
│                            │                            │ CurrentYearRevenue,        │        │                      │
│                            │                            │ PreviousYearRevenue, and   │        │                      │
│                            │                            │ YoYGrowthPercentage. It    │        │                      │
│                            │                            │ also gracefully handles    │        │                      │
│                            │                            │ the first year by yielding │        │                      │
│                            │                            │ NULL for missing prior     │        │                      │
│                            │                            │ revenue and avoids         │        │                      │
│                            │                            │ division by zero. No       │        │                      │
│                            │                            │ reviewer notes or          │        │                      │
│                            │                            │ intermediate planning are  │        │                      │
│                            │                            │ present in the output.,    │        │                      │
│                            │                            │ error=None)                │        │                      │
│                            │ Production SQL Quality     │ 0.8 (threshold=0.8,        │ PASSED │                      │
│                            │ [GEval]                    │ evaluation                 │        │                      │
│                            │                            │ model=gpt-5.4-mini,        │        │                      │
│                            │                            │ reason=The SQL is          │        │                      │
│                            │                            │ syntactically valid T-SQL  │        │                      │
│                            │                            │ and correctly uses a CTE,  │        │                      │
│                            │                            │ Sales.SalesOrderHeader,    │        │                      │
│                            │                            │ Sales.SalesTerritory, and  │        │                      │
│                            │                            │ LAG() to compute           │        │                      │
│                            │                            │ previous-year revenue with │        │                      │
│                            │                            │ NULL handling for the      │        │                      │
│                            │                            │ first year. It is also     │        │                      │
│                            │                            │ reasonably well formatted  │        │                      │
│                            │                            │ and includes inline        │        │                      │
│                            │                            │ comments. However, it      │        │                      │
│                            │                            │ reuses LAG() multiple      │        │                      │
│                            │                            │ times instead of computing │        │                      │
│                            │                            │ it once defensively, and   │        │                      │
│                            │                            │ the YoY percentage returns │        │                      │
│                            │                            │ NULL for the first year    │        │                      │
│                            │                            │ rather than explicitly     │        │                      │
│                            │                            │ handling it in a           │        │                      │
│                            │                            │ documented                 │        │                      │
│                            │                            │ business-friendly way;     │        │                      │
│                            │                            │ there are also no          │        │                      │
│                            │                            │ schema-tool placeholder    │        │                      │
│                            │                            │ issues. Overall it aligns  │        │                      │
│                            │                            │ strongly with the          │        │                      │
│                            │                            │ requirements., error=None) │        │                      │
│                            │ Query Efficiency [GEval]   │ 0.8 (threshold=0.8,        │ PASSED │                      │
│                            │                            │ evaluation                 │        │                      │
│                            │                            │ model=gpt-5.4-mini,        │        │                      │
│                            │                            │ reason=The query satisfies │        │                      │
│                            │                            │ the main acceptance        │        │                      │
│                            │                            │ criteria: it uses a CTE,   │        │                      │
│                            │                            │ explicitly selects needed  │        │                      │
│                            │                            │ columns, joins             │        │                      │
│                            │                            │ Sales.SalesOrderHeader to  │        │                      │
│                            │                            │ Sales.SalesTerritory, and  │        │                      │
│                            │                            │ uses LAG() to get the      │        │                      │
│                            │                            │ prior year's revenue with  │        │                      │
│                            │                            │ NULL handling for the      │        │                      │
│                            │                            │ first year. However, it    │        │                      │
│                            │                            │ does not follow the        │        │                      │
│                            │                            │ sargability guidance       │        │                      │
│                            │                            │ because it groups by       │        │                      │
│                            │                            │ YEAR(OrderDate), which     │        │                      │
│                            │                            │ wraps the date column in a │        │                      │
│                            │                            │ function instead of using  │        │                      │
│                            │                            │ a range predicate, though  │        │                      │
│                            │                            │ this requirement was not   │        │                      │
│                            │                            │ directly needed by the     │        │                      │
│                            │                            │ task. It also repeats the  │        │                      │
│                            │                            │ same LAG() expression      │        │                      │
│                            │                            │ multiple times in the YoY  │        │                      │
│                            │                            │ calculation instead of     │        │                      │
│                            │                            │ computing it once, which   │        │                      │
│                            │                            │ is less efficient.,        │        │                      │
│                            │                            │ error=None)                │        │                      │
│                            │ Security and Safety        │ 1.0 (threshold=1.0,        │ PASSED │                      │
│                            │ [GEval]                    │ evaluation                 │        │                      │
│                            │                            │ model=gpt-5.4-mini,        │        │                      │
│                            │                            │ reason=The SQL is          │        │                      │
│                            │                            │ read-only and consists     │        │                      │
│                            │                            │ only of a CTE followed by  │        │                      │
│                            │                            │ a SELECT, with no INSERT,  │        │                      │
│                            │                            │ UPDATE, DELETE, TRUNCATE,  │        │                      │
│                            │                            │ DROP, ALTER, CREATE, or    │        │                      │
│                            │                            │ dynamic EXEC/sp_executesql │        │                      │
│                            │                            │ usage. It also matches the │        │                      │
│                            │                            │ task requirements by using │        │                      │
│                            │                            │ Sales.SalesOrderHeader and │        │                      │
│                            │                            │ Sales.SalesTerritory,      │        │                      │
│                            │                            │ returning TerritoryName,   │        │                      │
│                            │                            │ SalesYear,                 │        │                      │
│                            │                            │ CurrentYearRevenue,        │        │                      │
│                            │                            │ PreviousYearRevenue, and   │        │                      │
│                            │                            │ YoYGrowthPercentage, and   │        │                      │
│                            │                            │ handling the first year    │        │                      │
│                            │                            │ with NULL via LAG().,      │        │                      │
│                            │                            │ error=None)                │        │                      │
│                            │ Schema Hallucination Free  │ 1.0 (threshold=0.9,        │ PASSED │                      │
│                            │ [GEval]                    │ evaluation                 │        │                      │
│                            │                            │ model=gpt-5.4-mini,        │        │                      │
│                            │                            │ reason=The SQL matches the │        │                      │
│                            │                            │ requirements well: it uses │        │                      │
│                            │                            │ the specified              │        │                      │
│                            │                            │ Sales.SalesOrderHeader and │        │                      │
│                            │                            │ Sales.SalesTerritory       │        │                      │
│                            │                            │ tables, includes a CTE for │        │                      │
│                            │                            │ annual revenue by          │        │                      │
│                            │                            │ territory, applies LAG()   │        │                      │
│                            │                            │ partitioned by territory   │        │                      │
│                            │                            │ and ordered by SalesYear,  │        │                      │
│                            │                            │ and returns the required   │        │                      │
│                            │                            │ fields TerritoryName,      │        │                      │
│                            │                            │ SalesYear,                 │        │                      │
│                            │                            │ CurrentYearRevenue,        │        │                      │
│                            │                            │ PreviousYearRevenue, and   │        │                      │
│                            │                            │ YoYGrowthPercentage. It    │        │                      │
│                            │                            │ also handles the first     │        │                      │
│                            │                            │ year with NULL and avoids  │        │                      │
│                            │                            │ division-by-zero. No       │        │                      │
│                            │                            │ invented or generic        │        │                      │
│                            │                            │ placeholder tables/columns │        │                      │
│                            │                            │ are present., error=None)  │        │                      │
│                            │ Maintainability [GEval]    │ 0.9 (threshold=0.7,        │ PASSED │                      │
│                            │                            │ evaluation                 │        │                      │
│                            │                            │ model=gpt-5.4-mini,        │        │                      │
│                            │                            │ reason=The query largely   │        │                      │
│                            │                            │ matches the requirements:  │        │                      │
│                            │                            │ it uses a CTE to aggregate │        │                      │
│                            │                            │ annual revenue by          │        │                      │
│                            │                            │ territory, joins           │        │                      │
│                            │                            │ Sales.SalesOrderHeader and │        │                      │
│                            │                            │ Sales.SalesTerritory with  │        │                      │
│                            │                            │ clear aliases, and         │        │                      │
│                            │                            │ computes LAG() plus        │        │                      │
│                            │                            │ YoYGrowthPercentage with   │        │                      │
│                            │                            │ NULL handling for the      │        │                      │
│                            │                            │ first year. The columns    │        │                      │
│                            │                            │ also have explicit         │        │                      │
│                            │                            │ aliases. However, the      │        │                      │
│                            │                            │ description is accurate    │        │                      │
│                            │                            │ but slightly incomplete    │        │                      │
│                            │                            │ because it omits the exact │        │                      │
│                            │                            │ acceptance criteria naming │        │                      │
│                            │                            │ of the previous-year field │        │                      │
│                            │                            │ as a returned output and   │        │                      │
│                            │                            │ could more clearly         │        │                      │
│                            │                            │ emphasize the grouped      │        │                      │
│                            │                            │ annual revenue step.       │        │                      │
│                            │                            │ Overall, strong alignment  │        │                      │
│                            │                            │ with only minor issues.,   │        │                      │
│                            │                            │ error=None)                │        │                      │
│                            │                            │                            │        │                      │
│ test_e2e_email_domain_dis… │                            │                            │        │ 100.0%               │
│                            │ Task Accuracy and          │ 0.9 (threshold=0.8,        │ PASSED │                      │
│                            │ Completion [GEval]         │ evaluation                 │        │                      │
│                            │                            │ model=gpt-5.4-mini,        │        │                      │
│                            │                            │ reason=The SQL matches the │        │                      │
│                            │                            │ request well: it extracts  │        │                      │
│                            │                            │ EmailDomain from           │        │                      │
│                            │                            │ Person.EmailAddress.Email… │        │                      │
│                            │                            │ using CHARINDEX and        │        │                      │
│                            │                            │ SUBSTRING, returns the     │        │                      │
│                            │                            │ required EmailDomain and   │        │                      │
│                            │                            │ DomainCount columns,       │        │                      │
│                            │                            │ groups by the extracted    │        │                      │
│                            │                            │ domain, and orders by      │        │                      │
│                            │                            │ frequency descending. The  │        │                      │
│                            │                            │ only minor issue is the    │        │                      │
│                            │                            │ added NULL/'@' filtering,  │        │                      │
│                            │                            │ which is reasonable and    │        │                      │
│                            │                            │ does not conflict with the │        │                      │
│                            │                            │ requirements. No reviewer  │        │                      │
│                            │                            │ notes or planning steps    │        │                      │
│                            │                            │ are present in the final   │        │                      │
│                            │                            │ code output., error=None)  │        │                      │
│                            │ Production SQL Quality     │ 0.8 (threshold=0.8,        │ PASSED │                      │
│                            │ [GEval]                    │ evaluation                 │        │                      │
│                            │                            │ model=gpt-5.4-mini,        │        │                      │
│                            │                            │ reason=The SQL is          │        │                      │
│                            │                            │ syntactically valid T-SQL  │        │                      │
│                            │                            │ and satisfies the          │        │                      │
│                            │                            │ acceptance criteria by     │        │                      │
│                            │                            │ returning EmailDomain and  │        │                      │
│                            │                            │ DomainCount, extracting    │        │                      │
│                            │                            │ the domain with            │        │                      │
│                            │                            │ SUBSTRING/CHARINDEX,       │        │                      │
│                            │                            │ grouping by it, and        │        │                      │
│                            │                            │ ordering by frequency. It  │        │                      │
│                            │                            │ also includes a defensive  │        │                      │
│                            │                            │ NULL/@ check and a brief   │        │                      │
│                            │                            │ inline comment. However,   │        │                      │
│                            │                            │ it does not demonstrate    │        │                      │
│                            │                            │ broader production-level   │        │                      │
│                            │                            │ defensive programming, and │        │                      │
│                            │                            │ it does not address the    │        │                      │
│                            │                            │ schema-tool requirement    │        │                      │
│                            │                            │ beyond using               │        │                      │
│                            │                            │ Person.EmailAddress; there │        │                      │
│                            │                            │ is no placeholder schema   │        │                      │
│                            │                            │ name, but the output lacks │        │                      │
│                            │                            │ evidence of schema         │        │                      │
│                            │                            │ validation or more robust  │        │                      │
│                            │                            │ safeguards., error=None)   │        │                      │
│                            │ Query Efficiency [GEval]   │ 0.8 (threshold=0.8,        │ PASSED │                      │
│                            │                            │ evaluation                 │        │                      │
│                            │                            │ model=gpt-5.4-mini,        │        │                      │
│                            │                            │ reason=The query meets the │        │                      │
│                            │                            │ task requirements by       │        │                      │
│                            │                            │ explicitly selecting       │        │                      │
│                            │                            │ EmailDomain and            │        │                      │
│                            │                            │ DomainCount, extracting    │        │                      │
│                            │                            │ the domain with SUBSTRING  │        │                      │
│                            │                            │ and CHARINDEX, grouping by │        │                      │
│                            │                            │ the derived domain, and    │        │                      │
│                            │                            │ ordering by count          │        │                      │
│                            │                            │ descending. It also avoids │        │                      │
│                            │                            │ SELECT * and does not use  │        │                      │
│                            │                            │ a correlated subquery.     │        │                      │
│                            │                            │ However, the WHERE clause  │        │                      │
│                            │                            │ is not meaningfully        │        │                      │
│                            │                            │ sargable because it        │        │                      │
│                            │                            │ applies CHARINDEX to the   │        │                      │
│                            │                            │ EmailAddress column, which │        │                      │
│                            │                            │ can limit index use, and   │        │                      │
│                            │                            │ the GROUP BY repeats the   │        │                      │
│                            │                            │ same expression instead of │        │                      │
│                            │                            │ using a more efficient     │        │                      │
│                            │                            │ derivation approach.,      │        │                      │
│                            │                            │ error=None)                │        │                      │
│                            │ Security and Safety        │ 1.0 (threshold=1.0,        │ PASSED │                      │
│                            │ [GEval]                    │ evaluation                 │        │                      │
│                            │                            │ model=gpt-5.4-mini,        │        │                      │
│                            │                            │ reason=The SQL is          │        │                      │
│                            │                            │ read-only and uses only a  │        │                      │
│                            │                            │ SELECT statement, with no  │        │                      │
│                            │                            │ INSERT, UPDATE, DELETE,    │        │                      │
│                            │                            │ TRUNCATE, DROP, ALTER,     │        │                      │
│                            │                            │ CREATE, or dynamic SQL. It │        │                      │
│                            │                            │ also matches the task by   │        │                      │
│                            │                            │ extracting the domain      │        │                      │
│                            │                            │ after '@' using SUBSTRING  │        │                      │
│                            │                            │ and CHARINDEX, grouping by │        │                      │
│                            │                            │ the extracted domain,      │        │                      │
│                            │                            │ counting rows as           │        │                      │
│                            │                            │ DomainCount, and ordering  │        │                      │
│                            │                            │ descending. The only minor │        │                      │
│                            │                            │ mismatch is that it        │        │                      │
│                            │                            │ queries                    │        │                      │
│                            │                            │ Person.EmailAddress rather │        │                      │
│                            │                            │ than a contact table name, │        │                      │
│                            │                            │ but the structure and      │        │                      │
│                            │                            │ intent align with the      │        │                      │
│                            │                            │ requirements., error=None) │        │                      │
│                            │ Schema Hallucination Free  │ 1.0 (threshold=0.9,        │ PASSED │                      │
│                            │ [GEval]                    │ evaluation                 │        │                      │
│                            │                            │ model=gpt-5.4-mini,        │        │                      │
│                            │                            │ reason=The SQL matches the │        │                      │
│                            │                            │ requirements well: it      │        │                      │
│                            │                            │ queries                    │        │                      │
│                            │                            │ Person.EmailAddress,       │        │                      │
│                            │                            │ extracts the domain from   │        │                      │
│                            │                            │ EmailAddress using         │        │                      │
│                            │                            │ CHARINDEX and SUBSTRING,   │        │                      │
│                            │                            │ returns EmailDomain and    │        │                      │
│                            │                            │ DomainCount, groups by the │        │                      │
│                            │                            │ derived domain, and orders │        │                      │
│                            │                            │ by frequency descending.   │        │                      │
│                            │                            │ No invented tables or      │        │                      │
│                            │                            │ placeholder columns        │        │                      │
│                            │                            │ appear. A minor difference │        │                      │
│                            │                            │ is the added NULL/@        │        │                      │
│                            │                            │ validation filter, but it  │        │                      │
│                            │                            │ is compatible with the     │        │                      │
│                            │                            │ task., error=None)         │        │                      │
│                            │ Maintainability [GEval]    │ 0.9 (threshold=0.7,        │ PASSED │                      │
│                            │                            │ evaluation                 │        │                      │
│                            │                            │ model=gpt-5.4-mini,        │        │                      │
│                            │                            │ reason=The query is        │        │                      │
│                            │                            │ well-structured, uses a    │        │                      │
│                            │                            │ clear table alias for      │        │                      │
│                            │                            │ Person.EmailAddress, and   │        │                      │
│                            │                            │ gives explicit aliases to  │        │                      │
│                            │                            │ the calculated domain and  │        │                      │
│                            │                            │ count columns. The         │        │                      │
│                            │                            │ description accurately     │        │                      │
│                            │                            │ explains extracting the    │        │                      │
│                            │                            │ domain after '@',          │        │                      │
│                            │                            │ grouping, and ordering by  │        │                      │
│                            │                            │ frequency. The main gap is │        │                      │
│                            │                            │ that the evaluation step   │        │                      │
│                            │                            │ asks for the description   │        │                      │
│                            │                            │ field to clearly explain   │        │                      │
│                            │                            │ the technical intent,      │        │                      │
│                            │                            │ which is satisfied, but    │        │                      │
│                            │                            │ the output does not show   │        │                      │
│                            │                            │ any JOINs, so aliasing     │        │                      │
│                            │                            │ guidance for JOINs is not  │        │                      │
│                            │                            │ applicable here.,          │        │                      │
│                            │                            │ error=None)                │        │                      │
│ Note: Use Confident AI     │                            │                            │        │                      │
│ with DeepEval to analyze   │                            │                            │        │                      │
│ failed test cases for more │                            │                            │        │                      │
│ details                    │                            │                            │        │                      │
└────────────────────────────┴────────────────────────────┴────────────────────────────┴────────┴──────────────────────┘

⚠ WARNING: No hyperparameters logged.
» Log hyperparameters to attribute prompts and models to your test runs.

================================================================================


✓ Evaluation completed 🎉! (time taken: 386.88s | token cost: 0.03163125 USD)
» Test Results (5 total tests):
   » Pass Rate: 60.0% | Passed: 3 | Failed: 2

 ================================================================================
 ```

 #### Результат для `deepeval test run tests/test_planner.py`

 ```
 ================================================================================


✓ Evaluation completed 🎉! (time taken: 386.88s | token cost: 0.03163125 USD)
» Test Results (5 total tests):
   » Pass Rate: 60.0% | Passed: 3 | Failed: 2

 ================================================================================

» Want to share evals with your team, or a place for your test cases to live? ❤️ 🏡
  » Run 'deepeval view' to analyze and save testing results on Confident AI.


PS C:\Users\Viktor\source\repos\MULTI-AGENT-SYSTEMS-course\course-project> deepeval test run tests/test_planner.py
.Running teardown with pytest sessionfinish...

============================================================================================= slowest 10 durations =============================================================================================
105.67s call     tests/test_planner.py::test_plan_alignment
99.96s call     tests/test_planner.py::test_plan_edge_cases
63.66s call     tests/test_planner.py::test_plan_has_queries
54.77s call     tests/test_planner.py::test_plan_quality

(6 durations < 0.005s hidden.  Use -vv to show these durations.)
4 passed, 4 warnings in 350.35s (0:05:50)
                                                                                                  Test Results
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┓
┃ Test case                                                      ┃ Metric                                      ┃ Score                                                          ┃ Status ┃ Overall Success Rate ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━┩
│ test_plan_quality                                              │                                             │                                                                │        │ 100.0%               │
│                                                                │ Plan Quality [GEval]                        │ 0.9 (threshold=0.7, evaluation model=gpt-5.4-mini, reason=The  │ PASSED │                      │
│                                                                │                                             │ output matches the requested plan structure and includes       │        │                      │
│                                                                │                                             │ relevant requirements with more than two topic-specific items  │        │                      │
│                                                                │                                             │ about counting active employees from HumanResources.Employee.  │        │                      │
│                                                                │                                             │ It also provides concrete acceptance criteria such as          │        │                      │
│                                                                │                                             │ returning one aggregated value, counting each BusinessEntityID │        │                      │
│                                                                │                                             │ once, and excluding inactive employees. The format is JSON,    │        │                      │
│                                                                │                                             │ aligning with the expected output shape., error=None)          │        │                      │
│                                                                │                                             │                                                                │        │                      │
│ test_plan_has_queries                                          │                                             │                                                                │        │ 100.0%               │
│                                                                │ Plan Has Tables and Joins [GEval]           │ 0.7 (threshold=0.7, evaluation model=gpt-5.4-mini, reason=The  │ PASSED │                      │
│                                                                │                                             │ response correctly identifies the main table,                  │        │                      │
│                                                                │                                             │ Sales.SalesOrderHeader, and includes the key fields needed for │        │                      │
│                                                                │                                             │ grouping and filtering, such as order date and Status. It also │        │                      │
│                                                                │                                             │ states the yearly aggregation, sorting, and the need to avoid  │        │                      │
│                                                                │                                             │ duplicate counting, which matches the summarization            │        │                      │
│                                                                │                                             │ requirement. However, it does not explicitly list all specific │        │                      │
│                                                                │                                             │ database tables if a detail table were required, and the       │        │                      │
│                                                                │                                             │ relationship between tables is only described conditionally    │        │                      │
│                                                                │                                             │ rather than as a clear join definition., error=None)           │        │                      │
│                                                                │                                             │                                                                │        │                      │
│ test_plan_edge_cases                                           │                                             │                                                                │        │ 100.0%               │
│                                                                │ Edge Case and Data Quality Handling [GEval] │ 0.7 (threshold=0.7, evaluation model=gpt-5.4-mini, reason=The  │ PASSED │                      │
│                                                                │                                             │ plan partially addresses the task by explicitly handling ties: │        │                      │
│                                                                │                                             │ it says to return all employees sharing the highest salary in  │        │                      │
│                                                                │                                             │ a department. It also mentions avoiding duplicate rows by      │        │                      │
│                                                                │                                             │ using only the latest department and pay records. However, it  │        │                      │
│                                                                │                                             │ does not explicitly discuss NULL handling in the relevant      │        │                      │
│                                                                │                                             │ columns, which is required by the evaluation steps, and the    │        │                      │
│                                                                │                                             │ query logic still leaves some ambiguity around null salary or  │        │                      │
│                                                                │                                             │ department values., error=None)                                │        │                      │
│                                                                │                                             │                                                                │        │                      │
│ test_plan_alignment                                            │                                             │                                                                │        │ 100.0%               │
│                                                                │ Requirements and Criteria Alignment [GEval] │ 1.0 (threshold=0.7, evaluation model=gpt-5.4-mini, reason=The  │ PASSED │                      │
│                                                                │                                             │ acceptance criteria closely mirror the requirements: they test │        │                      │
│                                                                │                                             │ use of Sales.SalesOrderHeader, TotalDue, filtering Status = 6, │        │                      │
│                                                                │                                             │ selecting the maximum year, monthly aggregation, MoM formula,  │        │                      │
│                                                                │                                             │ first-month null handling, zero-division safety, chronological │        │                      │
│                                                                │                                             │ ordering, and avoiding duplicate detail joins. They also       │        │                      │
│                                                                │                                             │ preserve the “latest year”/partial-year behavior without       │        │                      │
│                                                                │                                             │ adding new tables or business logic beyond the requirements.,  │        │                      │
│                                                                │                                             │ error=None)                                                    │        │                      │
│ Note: Use Confident AI with DeepEval to analyze failed test    │                                             │                                                                │        │                      │
│ cases for more details                                         │                                             │                                                                │        │                      │
└────────────────────────────────────────────────────────────────┴─────────────────────────────────────────────┴────────────────────────────────────────────────────────────────┴────────┴──────────────────────┘

⚠ WARNING: No hyperparameters logged.
» Log hyperparameters to attribute prompts and models to your test runs.

================================================================================


✓ Evaluation completed 🎉! (time taken: 353.63s | token cost: 0.00407625 USD)
» Test Results (4 total tests):
   » Pass Rate: 100.0% | Passed: 4 | Failed: 0

 ================================================================================
 ```

#### Результат для `deepeval test run tests/test_coder.py`

```
 ---------------------------------------------------------------------------------------------- Captured log call -----------------------------------------------------------------------------------------------
INFO     deepeval.evaluate.execute:execute.py:779 in _a_execute_llm_test_cases
============================================================================================= slowest 10 durations =============================================================================================
102.18s call     tests/test_coder.py::test_code_sql_best_practices
51.55s call     tests/test_coder.py::test_code_schema_compliance
23.06s call     tests/test_coder.py::test_code_logic_alignment
9.87s call     tests/test_coder.py::test_code_description_quality

(6 durations < 0.005s hidden.  Use -vv to show these durations.)
=========================================================================================== short test summary info ============================================================================================
FAILED tests/test_coder.py::test_code_schema_compliance - AssertionError: Metrics: Code Output Schema Compliance [GEval] (score: 0.6, threshold: 0.9, strict: False, error: None, reason: The response includes a source_code field with actual SQL and a description ...
FAILED tests/test_coder.py::test_code_logic_alignment - deepeval.errors.MissingTestCaseParamsError: 'actual_output' cannot be empty for the 'Code Logic Alignment with Requirements [GEval]' metric
2 failed, 2 passed, 4 warnings in 217.61s (0:03:37)
                                                                                                  Test Results
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┓
┃ Test case                                                    ┃ Metric                                         ┃ Score                                                        ┃ Status  ┃ Overall Success Rate ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━┩
│ test_code_schema_compliance                                  │                                                │                                                              │         │ 0.0%                 │
│                                                              │ Code Output Schema Compliance [GEval]          │ 0.6 (threshold=0.9, evaluation model=gpt-5.4-mini,           │ FAILED  │                      │
│                                                              │                                                │ reason=The response includes a source_code field with actual │         │                      │
│                                                              │                                                │ SQL and a description field explaining the joins,            │         │                      │
│                                                              │                                                │ aggregation, and null-region filter. However, it does not    │         │                      │
│                                                              │                                                │ include the required files_created field as a list of        │         │                      │
│                                                              │                                                │ filenames, so it fails one of the evaluation steps. The SQL  │         │                      │
│                                                              │                                                │ also uses SalesOrderDetail/LineTotal and territory tables    │         │                      │
│                                                              │                                                │ rather than the explicitly requested Sales and Region        │         │                      │
│                                                              │                                                │ tables, but the main issue is the missing field.,            │         │                      │
│                                                              │                                                │ error=None)                                                  │         │                      │
│                                                              │                                                │                                                              │         │                      │
│ test_code_sql_best_practices                                 │                                                │                                                              │         │ 100.0%               │
│                                                              │ SQL Code Quality and Best Practices [GEval]    │ 1.0 (threshold=0.7, evaluation model=gpt-5.4-mini,           │ PASSED  │                      │
│                                                              │                                                │ reason=The source_code is valid T-SQL: it uses SQL           │         │                      │
│                                                              │                                                │ Server-specific constructs like DATEADD, ROW_NUMBER, CTEs,   │         │                      │
│                                                              │                                                │ and schema-qualified tables. It also includes inline         │         │                      │
│                                                              │                                                │ comments explaining the date-window interpretation and       │         │                      │
│                                                              │                                                │ ranking logic, and the formatting/indentation is readable.   │         │                      │
│                                                              │                                                │ The query uses CTEs rather than nested subqueries for the    │         │                      │
│                                                              │                                                │ multi-step logic, which matches the evaluation steps well.,  │         │                      │
│                                                              │                                                │ error=None)                                                  │         │                      │
│                                                              │                                                │                                                              │         │                      │
│ test_code_description_quality                                │                                                │                                                              │         │ 100.0%               │
│                                                              │ Code Description Completeness [GEval]          │ 1.0 (threshold=0.7, evaluation model=gpt-5.4-mini,           │ PASSED  │                      │
│                                                              │                                                │ reason=The description is not vague and clearly explains the │         │                      │
│                                                              │                                                │ core logic: joining SalesOrderHeader, SalesOrderDetail,      │         │                      │
│                                                              │                                                │ Product, ProductSubcategory, and ProductCategory, filtering  │         │                      │
│                                                              │                                                │ to 2013 and Bikes, and aggregating LineTotal and OrderQty.   │         │                      │
│                                                              │                                                │ It also mentions key handling choices like the date-range    │         │                      │
│                                                              │                                                │ filter for the year and grouping by CategoryName. ,          │         │                      │
│                                                              │                                                │ error=None)                                                  │         │                      │
│                                                              │                                                │                                                              │         │                      │
│ test_code_logic_alignment                                    │                                                │                                                              │         │ 0.0%                 │
│                                                              │ Code Logic Alignment with Requirements [GEval] │ None (threshold=0.8, evaluation model=gpt-5.4-mini,          │ ERRORED │                      │
│                                                              │                                                │ reason=None, error='actual_output' cannot be empty for the   │         │                      │
│                                                              │                                                │ 'Code Logic Alignment with Requirements [GEval]' metric)     │         │                      │
│ Note: Use Confident AI with DeepEval to analyze failed test  │                                                │                                                              │         │                      │
│ cases for more details                                       │                                                │                                                              │         │                      │
└──────────────────────────────────────────────────────────────┴────────────────────────────────────────────────┴──────────────────────────────────────────────────────────────┴─────────┴──────────────────────┘

⚠ WARNING: No hyperparameters logged.
» Log hyperparameters to attribute prompts and models to your test runs.

================================================================================


✓ Evaluation completed 🎉! (time taken: 223.15s | token cost: 0.00295575 USD)
» Test Results (4 total tests):
   » Pass Rate: 50.0% | Passed: 2 | Failed: 2

 ================================================================================
```

#### Результат для `deepeval test run tests/test_reviewer.py`

```
 ---------------------------------------------------------------------------------------------- Captured log call -----------------------------------------------------------------------------------------------
INFO     deepeval.evaluate.execute:execute.py:779 in _a_execute_llm_test_cases
============================================================================================= slowest 10 durations =============================================================================================
16.75s call     tests/test_reviewer.py::test_reviewer_spec_alignment_missing_filter
13.30s call     tests/test_reviewer.py::test_reviewer_bug_detection_divide_by_zero
7.23s call     tests/test_reviewer.py::test_reviewer_schema_compliance_approved

(6 durations < 0.005s hidden.  Use -vv to show these durations.)
=========================================================================================== short test summary info ============================================================================================
FAILED tests/test_reviewer.py::test_reviewer_spec_alignment_missing_filter - AssertionError: Metrics: Specification Adherence Validation [GEval] (score: 0.1, threshold: 0.8, strict: False, error: None, reason: The review correctly identifies the missing OrderDate year filter for 2...
1 failed, 2 passed, 4 warnings in 66.27s (0:01:06)
                                                                                                  Test Results
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┓
┃ Test case                                                      ┃ Metric                                     ┃ Score                                                           ┃ Status ┃ Overall Success Rate ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━┩
│ test_reviewer_schema_compliance_approved                       │                                            │                                                                 │        │ 100.0%               │
│                                                                │ Reviewer Output Schema Compliance [GEval]  │ 1.0 (threshold=0.9, evaluation model=gpt-5.4-mini, reason=The   │ PASSED │                      │
│                                                                │                                            │ output matches the evaluation steps: verdict is exactly         │        │                      │
│                                                                │                                            │ APPROVED, issues and suggestions are empty lists, and score is  │        │                      │
│                                                                │                                            │ a float within 0.0 to 1.0. It also fits the SQL review task     │        │                      │
│                                                                │                                            │ because the query returns one column named TotalSales and       │        │                      │
│                                                                │                                            │ computes the total sales amount with SUM(LineTotal).,           │        │                      │
│                                                                │                                            │ error=None)                                                     │        │                      │
│                                                                │                                            │                                                                 │        │                      │
│ test_reviewer_bug_detection_divide_by_zero                     │                                            │                                                                 │        │ 100.0%               │
│                                                                │ Bug and Edge Case Detection [GEval]        │ 0.9 (threshold=0.8, evaluation model=gpt-5.4-mini, reason=The   │ PASSED │                      │
│                                                                │                                            │ review correctly identified major issues relevant to the        │        │                      │
│                                                                │                                            │ specification: it flagged the missing NULLIF() safeguard for    │        │                      │
│                                                                │                                            │ divide-by-zero and noted that the query uses the wrong source   │        │                      │
│                                                                │                                            │ table/columns, which means it does not properly calculate       │        │                      │
│                                                                │                                            │ conversion rate by TerritoryID. It also pointed out integer     │        │                      │
│                                                                │                                            │ division risk and the lack of correct joining/combining of      │        │                      │
│                                                                │                                            │ order and visit data, which aligns with the requirement to      │        │                      │
│                                                                │                                            │ return TerritoryID and ConversionRate. However, it did not      │        │                      │
│                                                                │                                            │ explicitly analyze the exact SQL syntax in depth beyond these   │        │                      │
│                                                                │                                            │ flaws., error=None)                                             │        │                      │
│                                                                │ Actionable Feedback Quality [GEval]        │ 0.9 (threshold=0.7, evaluation model=gpt-5.4-mini, reason=The   │ PASSED │                      │
│                                                                │                                            │ response includes concrete SQL fixes in the suggestions, such   │        │                      │
│                                                                │                                            │ as using the correct source tables, casting to decimal to avoid │        │                      │
│                                                                │                                            │ integer division, and wrapping the denominator with NULLIF(..., │        │                      │
│                                                                │                                            │ 0). These are specific and non-vague, matching the evaluation   │        │                      │
│                                                                │                                            │ steps. It also proposes a join/CTE pattern to aggregate by      │        │                      │
│                                                                │                                            │ TerritoryID, which is directly relevant to the requirement.,    │        │                      │
│                                                                │                                            │ error=None)                                                     │        │                      │
│                                                                │                                            │                                                                 │        │                      │
│ test_reviewer_spec_alignment_missing_filter                    │                                            │                                                                 │        │ 50.0%                │
│                                                                │ Specification Adherence Validation [GEval] │ 0.1 (threshold=0.8, evaluation model=gpt-5.4-mini, reason=The   │ FAILED │                      │
│                                                                │                                            │ review correctly identifies the missing OrderDate year filter   │        │                      │
│                                                                │                                            │ for 2013 and notes that the existing category filter and output │        │                      │
│                                                                │                                            │ aliases CategoryName and TotalRevenue are correct. However, it  │        │                      │
│                                                                │                                            │ does not explicitly compare the SQL against all acceptance      │        │                      │
│                                                                │                                            │ criteria in a structured way, and the score appears as 0.45     │        │                      │
│                                                                │                                            │ rather than an integer as required by the evaluation format.,   │        │                      │
│                                                                │                                            │ error=None)                                                     │        │                      │
│                                                                │ Actionable Feedback Quality [GEval]        │ 1.0 (threshold=0.7, evaluation model=gpt-5.4-mini, reason=The   │ PASSED │                      │
│                                                                │                                            │ output identifies the missing 2013 OrderDate filter and gives a │        │                      │
│                                                                │                                            │ concrete SQL fix using a sargable date range, which matches the │        │                      │
│                                                                │                                            │ evaluation steps’ requirement for specific syntax suggestions.  │        │                      │
│                                                                │                                            │ It also avoids vague advice and explicitly ties the issue to    │        │                      │
│                                                                │                                            │ the acceptance criterion for Bikes revenue in 2013, though it   │        │                      │
│                                                                │                                            │ includes extra debugging detail not required by the task.,      │        │                      │
│                                                                │                                            │ error=None)                                                     │        │                      │
│ Note: Use Confident AI with DeepEval to analyze failed test    │                                            │                                                                 │        │                      │
│ cases for more details                                         │                                            │                                                                 │        │                      │
└────────────────────────────────────────────────────────────────┴────────────────────────────────────────────┴─────────────────────────────────────────────────────────────────┴────────┴──────────────────────┘

⚠ WARNING: No hyperparameters logged.
» Log hyperparameters to attribute prompts and models to your test runs.

================================================================================


✓ Evaluation completed 🎉! (time taken: 70.27s | token cost: 0.00492225 USD)
» Test Results (3 total tests):
   » Pass Rate: 66.67% | Passed: 2 | Failed: 1

 ================================================================================
```

#### Результат для `deepeval test run tests/test_tools.py`

```
 ---------------------------------------------------------------------------------------------- Captured log call -----------------------------------------------------------------------------------------------
INFO     deepeval.evaluate.execute:execute.py:779 in _a_execute_llm_test_cases
============================================================================================= slowest 10 durations =============================================================================================
127.19s call     tests/test_tools.py::test_planner_tools
6.08s call     tests/test_tools.py::test_coder_tools
5.64s call     tests/test_tools.py::test_reviewer_tools
2.27s call     tests/test_tools.py::test_planner_tools_error_request

(6 durations < 0.005s hidden.  Use -vv to show these durations.)
=========================================================================================== short test summary info ============================================================================================
FAILED tests/test_tools.py::test_planner_tools - AssertionError: Metrics: Tool Correctness (score: 0.5, threshold: 0.7, strict: False, error: None, reason: [
FAILED tests/test_tools.py::test_coder_tools - AssertionError: Metrics: Tool Correctness (score: 0.6666666666666666, threshold: 0.7, strict: False, error: None, reason: [
2 failed, 2 passed, 4 warnings in 173.39s (0:02:53)
                                                                                                  Test Results
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┓
┃ Test case                                                                    ┃ Metric           ┃ Score                                                                       ┃ Status ┃ Overall Success Rate ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━┩
│ test_planner_tools                                                           │                  │                                                                             │        │ 0.0%                 │
│                                                                              │ Tool Correctness │ 0.5 (threshold=0.7, evaluation model=n/a, reason=[                          │ FAILED │                      │
│                                                                              │                  │          Tool Calling Reason: Incomplete tool usage: missing tools          │        │                      │
│                                                                              │                  │ [ToolCall(                                                                  │        │                      │
│                                                                              │                  │     name="get_table_structure"                                              │        │                      │
│                                                                              │                  │ ), ToolCall(                                                                │        │                      │
│                                                                              │                  │     name="get_sample_rows"                                                  │        │                      │
│                                                                              │                  │ )]; expected ['list_schemas_and_tables', 'knowledge_search',                │        │                      │
│                                                                              │                  │ 'get_table_structure', 'get_sample_rows'], called ['knowledge_search',      │        │                      │
│                                                                              │                  │ 'list_schemas_and_tables']. See more details above.                         │        │                      │
│                                                                              │                  │          Tool Selection Reason: No available tools were provided to assess  │        │                      │
│                                                                              │                  │ tool selection criteria                                                     │        │                      │
│                                                                              │                  │ ]                                                                           │        │                      │
│                                                                              │                  │ , error=None)                                                               │        │                      │
│                                                                              │                  │                                                                             │        │                      │
│ test_planner_tools_error_request                                             │                  │                                                                             │        │ 100.0%               │
│                                                                              │ Tool Correctness │ 1.0 (threshold=0.7, evaluation model=n/a, reason=[                          │ PASSED │                      │
│                                                                              │                  │          Tool Calling Reason: All expected tools                            │        │                      │
│                                                                              │                  │ ['ask_user_for_clarification'] were called (order not considered).          │        │                      │
│                                                                              │                  │          Tool Selection Reason: No available tools were provided to assess  │        │                      │
│                                                                              │                  │ tool selection criteria                                                     │        │                      │
│                                                                              │                  │ ]                                                                           │        │                      │
│                                                                              │                  │ , error=None)                                                               │        │                      │
│                                                                              │                  │                                                                             │        │                      │
│ test_coder_tools                                                             │                  │                                                                             │        │ 0.0%                 │
│                                                                              │ Tool Correctness │ 0.67 (threshold=0.7, evaluation model=n/a, reason=[                         │ FAILED │                      │
│                                                                              │                  │          Tool Calling Reason: Incomplete tool usage: missing tools          │        │                      │
│                                                                              │                  │ [ToolCall(                                                                  │        │                      │
│                                                                              │                  │     name="get_sql_execution_plan"                                           │        │                      │
│                                                                              │                  │ )]; expected ['get_table_structure', 'execute_sql_query',                   │        │                      │
│                                                                              │                  │ 'get_sql_execution_plan'], called ['get_table_structure',                   │        │                      │
│                                                                              │                  │ 'execute_sql_query']. See more details above.                               │        │                      │
│                                                                              │                  │          Tool Selection Reason: No available tools were provided to assess  │        │                      │
│                                                                              │                  │ tool selection criteria                                                     │        │                      │
│                                                                              │                  │ ]                                                                           │        │                      │
│                                                                              │                  │ , error=None)                                                               │        │                      │
│                                                                              │                  │                                                                             │        │                      │
│ test_reviewer_tools                                                          │                  │                                                                             │        │ 100.0%               │
│                                                                              │ Tool Correctness │ 1.0 (threshold=0.7, evaluation model=n/a, reason=[                          │ PASSED │                      │
│                                                                              │                  │          Tool Calling Reason: All expected tools ['execute_sql_query',      │        │                      │
│                                                                              │                  │ 'get_sql_execution_plan'] were called (order not considered).               │        │                      │
│                                                                              │                  │          Tool Selection Reason: No available tools were provided to assess  │        │                      │
│                                                                              │                  │ tool selection criteria                                                     │        │                      │
│                                                                              │                  │ ]                                                                           │        │                      │
│                                                                              │                  │ , error=None)                                                               │        │                      │
│ Note: Use Confident AI with DeepEval to analyze failed test cases for more   │                  │                                                                             │        │                      │
│ details                                                                      │                  │                                                                             │        │                      │
└──────────────────────────────────────────────────────────────────────────────┴──────────────────┴─────────────────────────────────────────────────────────────────────────────┴────────┴──────────────────────┘

⚠ WARNING: No hyperparameters logged.
» Log hyperparameters to attribute prompts and models to your test runs.

================================================================================


✓ Evaluation completed 🎉! (time taken: 176.79s | token cost: None)
» Test Results (4 total tests):
   » Pass Rate: 50.0% | Passed: 2 | Failed: 2

 ================================================================================
 ```