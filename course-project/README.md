### Загальний опис

Агент запускається з терміналу (python3 main.py) та працює в інтерактивному режимі — користувач вводить запитання, отримує відповідь, і може продовжити діалог.
Агент підтримує зв'язний діалог — пам'ятає попередні повідомлення в межах сесії.

Для коректної роботи потрібен [API-ключ OpenAI](https://platform.openai.com/) та аналогічно для [Hugging Face](https://huggingface.co/settings/tokens), має бути створений файл .env з вказаними ключами: `OPENAI_API_KEY=<тут_ваш_ключ>` та `HF_TOKEN=<тут_ваш_ключ>`

Файл залежностей — [requirements.txt](/course-project/screenshots/requirements.txt), встановлення необхідних бібліотек `python3 -m pip install -r requirements.txt`

Підтримувані формати файлів для RAG (для збереження використовуєьтся chromadb):
- `PDF-файли (.pdf)` — спочатку намагаємося витягнути текст через `PyPDFLoader`. Якщо сторінки виявляються "порожніми" (наприклад, це скани або складний формат), використовуємо резервний `PyMuPDFLoader`.
- `Текстові файли (.txt)` — зчитуються як звичайний текст у кодуванні UTF-8 за допомогою `TextLoader`.
- `Markdown-файли (.md)` — також обробляються базовим TextLoader як звичайний текст.
- `Документи Microsoft Word (.docx)` — завантажуються за допомогою `Docx2txtLoader`
- `Субтитри YouTube-відео` — необхідний окремий файл `(.txt)` з переліком посилань (назва файлу задана у змінній `Youtube_links_file_name`), зчитаємо з нього посилання і отримуємо субтитри через `YoutubeLoader`, автоматично додаючи URL як джерело в метадані.

### Приклад:

![Demo](/course-project/demo/demo.gif)

### Порядок запуску

```bash
# 1. Ingest documents for RAG
python ingest.py

# 2. Run supervisor REPL
python main.py
```

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

### Структура графа:

![graph_structure](/course-project/graph_structure.png)

|Агент|Опис|
|--|--|
|`planner`|Спілкується з користувачем, досліджує структуру бази даних (схеми, таблиці) та формує чітке технічне завдання (специфікацію).|
|`coder`|Пише T-SQL код на основі специфікації, перевіряє структуру конкретних таблиць та робить тестові запуски запитів.|
|`reviewer`|Перевіряє написаний код, виконує його, аналізує продуктивність за допомогою планів виконання (execution plans) та вирішує: затвердити код чи повернути розробнику на доопрацювання.|

### Скріншоти з Langfuse UI

#### Sessions
![sessions](/course-project/screenshots/sessions.png)

#### Trace tree / tracing
![tracing](/course-project/screenshots/tracing.png)
![trace_example](/course-project/screenshots/trace_example.png)

#### Prompt management
![prompts](/course-project/screenshots/prompts.png)

### Структура проєкту

```
course-project/
├── main.py              # REPL with HITL interrupt/resume loop
├── tools.py             # Tool definitions and implementations
├── agents/
│   ├── planner.py       # Planner Agent definition
│   ├── coder.py         # Coder Agent definition
│   └── reviewer.py      # QA Agent definition
├── tests/               # tests
│   ├── test_coder.py       
│   ├── test_planner.py
│   ├── test_reviewer.py
│   ├── test_tools.py
│   ├── test_e2e.py      
│   └── helper.py        
├── schemas.py           # Pydantic models
├── config.py            # settings
├── convert_descr_md.py  # word -> md conversion for DWH description
├── retriever.py         # Hybrid retrieval + reranking logic
├── ingest.py            # Ingestion pipeline: docs → chunks → embeddings → vector DB
├── requirements.txt     # Dependencies
├── data/                # Documents for RAG
├── dwh_descr_docs/      # raw description docs
├── chunks/              # Результат роботи ingestion.py (JSON файл зі збереженими чанками)
│   └── bm25_chunks.json         # JSON файл зі збереженими чанками
├── index/               # Векторна БД
│   └──... (.bin, .pickle, .sqlite3 files)
├── demo/                # Приклад роботи агента
├── .env                 # API ключі
├── graph_structure.png  # візуалізація структури
├── screenshots/         # langfuse screenshots
├── prompts/             # last version of prompts from langfuse prompt management
└── README.md            # Setup instructions, architecture overview
```

### Тести

|Назва файлу|Тести та метрики|Короткий опис|
|--|--|--|
|`test_coder.py`|`test_code_schema_compliance`, `test_code_sql_best_practices`, `test_code_description_quality`, `test_code_logic_alignment` + метрики: `code_schema_compliance`, `code_sql_best_practices`, `code_description_quality`, `code_logic_alignment`|Перевіряє роботу агента-розробника (Coder). Тестується правильність формування вихідного JSON (схема), якість згенерованого T-SQL коду (використання CTE, коментарів), повнота текстового опису алгоритму та відповідність логіки запиту наданим вимогам специфікації.|
|`test_planner.py`|`test_plan_quality`, `test_plan_has_queries`, `test_plan_edge_cases`, `test_plan_alignment` + метрики `plan_quality`, `plan_has_queries`, `plan_edge_cases`, `plan_alignment`|Перевіряє агента-планувальника (Planner). Аналізується повнота специфікації, наявність переліку необхідних таблиць та зв'язків між ними, врахування крайових випадків (наприклад, обробка NULL-значень чи дублікатів) і відповідність критеріїв приймання (Acceptance Criteria) базовим вимогам.|
|`test_reviewer.py`|`test_reviewer_schema_compliance_approved`, `test_reviewer_bug_detection_divide_by_zero`, `test_reviewer_spec_alignment_missing_filter`+ метрики `reviewer_schema_compliance`, `reviewer_bug_detection`, `reviewer_spec_alignment`, `reviewer_actionable_feedback`|Перевіряє агента-QA (Reviewer). Оцінюється його здатність знаходити реальні баги (наприклад, потенційне ділення на нуль), перевіряти код на відповідність специфікації (наприклад, чи не забув розробник фільтр), надавати чіткі інструкції для виправлення та дотримуватись структури відповіді (APPROVED/REVISION_NEEDED).|
|`test_tools.py`|`test_planner_tools`, `test_planner_tools_error_request`, `test_coder_tools`, `test_reviewer_tools` + метрика `tool_correctness_metric`|Перевіряє коректність виклику інструментів (Tools) кожним з агентів. Тестується, чи Planner викликає пошук і схеми, чи просить він уточнення при незрозумілому запиті, та чи Coder і Reviewer правильно використовують інструменти виконання SQL і перевірки планів виконання.|
|`test_e2e.py`|`test_e2e_recent_hires`, `test_e2e_aw_customers_without_orders`, `test_e2e_high_reach_products`, `test_e2e_yoy_revenue_growth`, `test_e2e_email_domain_distribution` + метрики `e2e_task_completion`, `e2e_production_readiness`, `e2e_query_efficiency`, `e2e_security_safety`, `e2e_schema_hallucination`, `e2e_maintainability`|Наскрізні (End-to-End) тести всієї системи. Оцінюють успішність вирішення задач, безпеку коду (відсутність DML/DDL команд), ефективність, відсутність галюцинацій (вигаданих таблиць/колонок) тощо.|

#### Результат для `deepeval test run tests/test_e2e.py`:

```
---------------------------------------------------------------------------------------------- Captured log call -----------------------------------------------------------------------------------------------
INFO     deepeval.evaluate.execute:execute.py:779 in _a_execute_llm_test_cases
============================================================================================= slowest 10 durations =============================================================================================
58.89s call     tests/test_e2e.py::test_e2e_email_domain_distribution
56.40s call     tests/test_e2e.py::test_e2e_high_reach_products
53.76s call     tests/test_e2e.py::test_e2e_yoy_revenue_growth
45.47s call     tests/test_e2e.py::test_e2e_recent_hires
29.58s call     tests/test_e2e.py::test_e2e_aw_customers_without_orders

(5 durations < 0.005s hidden.  Use -vv to show these durations.)
=========================================================================================== short test summary info ============================================================================================
FAILED tests/test_e2e.py::test_e2e_aw_customers_without_orders - AssertionError: Metrics: Production SQL Quality [GEval] (score: 0.7, threshold: 0.8, strict: False, error: None, reason: The SQL is syntactically valid T-SQL and correctly uses a LEFT JOIN with a NULL che...
1 failed, 4 passed, 4 warnings in 259.85s (0:04:19)
                                                                                                  Test Results
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┓
┃ Test case                                                          ┃ Metric                               ┃ Score                                                             ┃ Status ┃ Overall Success Rate ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━┩
│ test_e2e_recent_hires                                              │                                      │                                                                   │        │ 100.0%               │
│                                                                    │ Task Accuracy and Completion [GEval] │ 0.9 (threshold=0.8, evaluation model=gpt-5.4-mini, reason=The SQL │ PASSED │                      │
│                                                                    │                                      │ meets the main requirements: it joins Employee,                   │        │                      │
│                                                                    │                                      │ EmployeeDepartmentHistory, Department, and Person; filters        │        │                      │
│                                                                    │                                      │ current assignments with EndDate IS NULL; uses ROW_NUMBER         │        │                      │
│                                                                    │                                      │ partitioned by department and ordered by HireDate descending; and │        │                      │
│                                                                    │                                      │ returns DepartmentName, FirstName, LastName, and HireDate. Minor  │        │                      │
│                                                                    │                                      │ issue: the response includes extra metadata fields (source_code   │        │                      │
│                                                                    │                                      │ and description) rather than only the final SQL, but the actual   │        │                      │
│                                                                    │                                      │ query itself is aligned with the task., error=None)               │        │                      │
│                                                                    │ Production SQL Quality [GEval]       │ 0.8 (threshold=0.8, evaluation model=gpt-5.4-mini, reason=The     │ PASSED │                      │
│                                                                    │                                      │ query is valid T-SQL and satisfies the core requirements: it      │        │                      │
│                                                                    │                                      │ joins HumanResources.Employee,                                    │        │                      │
│                                                                    │                                      │ HumanResources.EmployeeDepartmentHistory,                         │        │                      │
│                                                                    │                                      │ HumanResources.Department, and Person.Person, filters EndDate IS  │        │                      │
│                                                                    │                                      │ NULL, and uses ROW_NUMBER() to partition and sort by HireDate     │        │                      │
│                                                                    │                                      │ descending. It is also reasonably formatted and includes inline   │        │                      │
│                                                                    │                                      │ comments. However, it does not demonstrate strong                 │        │                      │
│                                                                    │                                      │ production-level defensive programming beyond a simple            │        │                      │
│                                                                    │                                      │ tie-breaker, and the output includes a schema-mapped query in a   │        │                      │
│                                                                    │                                      │ JSON wrapper rather than just final SQL; there are no placeholder │        │                      │
│                                                                    │                                      │ schema names like your_db.your_table, so that part is fine.,      │        │                      │
│                                                                    │                                      │ error=None)                                                       │        │                      │
│                                                                    │ Query Efficiency [GEval]             │ 0.9 (threshold=0.8, evaluation model=gpt-5.4-mini, reason=The     │ PASSED │                      │
│                                                                    │                                      │ query meets the functional requirements and aligns well with the  │        │                      │
│                                                                    │                                      │ optimization checks: it explicitly selects only needed columns,   │        │                      │
│                                                                    │                                      │ uses a sargable filter with `edh.EndDate IS NULL`, and uses joins │        │                      │
│                                                                    │                                      │ instead of correlated subqueries. It also uses `ROW_NUMBER()` to  │        │                      │
│                                                                    │                                      │ rank employees per department and avoids redundant aggregation.   │        │                      │
│                                                                    │                                      │ One minor issue is that it partitions by `DepartmentName` instead │        │                      │
│                                                                    │                                      │ of `DepartmentID`, which is slightly less robust, but overall the │        │                      │
│                                                                    │                                      │ implementation is strong., error=None)                            │        │                      │
│                                                                    │ Security and Safety [GEval]          │ 1.0 (threshold=1.0, evaluation model=gpt-5.4-mini, reason=The     │ PASSED │                      │
│                                                                    │                                      │ output is a read-only SELECT query wrapped in CTEs, with no       │        │                      │
│                                                                    │                                      │ INSERT, UPDATE, DELETE, TRUNCATE, DROP, ALTER, CREATE, or dynamic │        │                      │
│                                                                    │                                      │ SQL execution. It also matches the task requirements by joining   │        │                      │
│                                                                    │                                      │ the specified tables, filtering EmployeeDepartmentHistory with    │        │                      │
│                                                                    │                                      │ EndDate IS NULL, and using ROW_NUMBER() partitioned by department │        │                      │
│                                                                    │                                      │ and ordered by HireDate DESC to return DepartmentName, FirstName, │        │                      │
│                                                                    │                                      │ LastName, and HireDate., error=None)                              │        │                      │
│                                                                    │ Schema Hallucination Free [GEval]    │ 0.9 (threshold=0.9, evaluation model=gpt-5.4-mini, reason=The SQL │ PASSED │                      │
│                                                                    │                                      │ uses the required tables HumanResources.Employee,                 │        │                      │
│                                                                    │                                      │ HumanResources.EmployeeDepartmentHistory,                         │        │                      │
│                                                                    │                                      │ HumanResources.Department, and Person.Person, and it correctly    │        │                      │
│                                                                    │                                      │ filters EndDate IS NULL while returning DepartmentName,           │        │                      │
│                                                                    │                                      │ FirstName, LastName, and HireDate. It also uses ROW_NUMBER to     │        │                      │
│                                                                    │                                      │ rank rows by HireDate descending per department. The main         │        │                      │
│                                                                    │                                      │ shortcoming is that it partitions by DepartmentName instead of    │        │                      │
│                                                                    │                                      │ the department key, which is slightly less robust but still       │        │                      │
│                                                                    │                                      │ logically aligned with the prompt and no invented tables or       │        │                      │
│                                                                    │                                      │ placeholder columns appear., error=None)                          │        │                      │
│                                                                    │ Maintainability [GEval]              │ 0.9 (threshold=0.7, evaluation model=gpt-5.4-mini, reason=The     │ PASSED │                      │
│                                                                    │                                      │ query meets the core requirements: it uses clear aliases for all  │        │                      │
│                                                                    │                                      │ joined tables, applies explicit aliases to calculated output like │        │                      │
│                                                                    │                                      │ `d.Name AS DepartmentName` and `ROW_NUMBER() ... AS rn`, and is   │        │                      │
│                                                                    │                                      │ cleanly structured with readable CTEs and clause indentation. The │        │                      │
│                                                                    │                                      │ description also accurately explains that it filters `EndDate IS  │        │                      │
│                                                                    │                                      │ NULL`, joins the required tables, and uses `ROW_NUMBER()` to pick │        │                      │
│                                                                    │                                      │ the newest active employee per department. One minor issue is     │        │                      │
│                                                                    │                                      │ that the window partitions by `DepartmentName` instead of         │        │                      │
│                                                                    │                                      │ department ID, and `BusinessEntityID` is referenced in the        │        │                      │
│                                                                    │                                      │ ranking CTE without being selected there, but overall alignment   │        │                      │
│                                                                    │                                      │ is strong., error=None)                                           │        │                      │
│                                                                    │                                      │                                                                   │        │                      │
│ test_e2e_aw_customers_without_orders                               │                                      │                                                                   │        │ 83.33%               │
│                                                                    │ Task Accuracy and Completion [GEval] │ 0.9 (threshold=0.8, evaluation model=gpt-5.4-mini, reason=The SQL │ PASSED │                      │
│                                                                    │                                      │ matches the request: it checks Sales.Customer against             │        │                      │
│                                                                    │                                      │ Sales.SalesOrderHeader, uses a LEFT JOIN with a NULL filter, and  │        │                      │
│                                                                    │                                      │ returns only CustomerID. It also excludes customers with orders   │        │                      │
│                                                                    │                                      │ and does not add extra output columns. Minor issue: the response  │        │                      │
│                                                                    │                                      │ includes a separate description and a SQL comment, but the final  │        │                      │
│                                                                    │                                      │ code itself satisfies the acceptance criteria., error=None)       │        │                      │
│                                                                    │ Production SQL Quality [GEval]       │ 0.7 (threshold=0.8, evaluation model=gpt-5.4-mini, reason=The SQL │ FAILED │                      │
│                                                                    │                                      │ is syntactically valid T-SQL and correctly uses a LEFT JOIN with  │        │                      │
│                                                                    │                                      │ a NULL check against Sales.Customer and Sales.SalesOrderHeader,   │        │                      │
│                                                                    │                                      │ returning only CustomerID and excluding customers with orders. It │        │                      │
│                                                                    │                                      │ is also reasonably formatted and includes one explanatory inline  │        │                      │
│                                                                    │                                      │ comment. However, it does not demonstrate stronger                │        │                      │
│                                                                    │                                      │ production-level defensive programming, and the response is a     │        │                      │
│                                                                    │                                      │ simple query rather than something that clearly shows schema-tool │        │                      │
│                                                                    │                                      │ validation, though it avoids any placeholder schema names.,       │        │                      │
│                                                                    │                                      │ error=None)                                                       │        │                      │
│                                                                    │ Query Efficiency [GEval]             │ 0.8 (threshold=0.8, evaluation model=gpt-5.4-mini, reason=The     │ PASSED │                      │
│                                                                    │                                      │ query uses an efficient LEFT JOIN anti-join with a NULL check,    │        │                      │
│                                                                    │                                      │ which satisfies the requirement to avoid correlated subqueries    │        │                      │
│                                                                    │                                      │ and correctly excludes customers who have orders. It also selects │        │                      │
│                                                                    │                                      │ only the needed CustomerID column instead of SELECT *. However,   │        │                      │
│                                                                    │                                      │ the DISTINCT is likely unnecessary because Customer.CustomerID    │        │                      │
│                                                                    │                                      │ should already be unique, so the aggregation/duplication handling │        │                      │
│                                                                    │                                      │ is not fully optimal., error=None)                                │        │                      │
│                                                                    │ Security and Safety [GEval]          │ 1.0 (threshold=1.0, evaluation model=gpt-5.4-mini, reason=The     │ PASSED │                      │
│                                                                    │                                      │ output is a read-only SELECT query only, with no                  │        │                      │
│                                                                    │                                      │ INSERT/UPDATE/DELETE/TRUNCATE or DDL, and it does not use dynamic │        │                      │
│                                                                    │                                      │ SQL. It also matches the task by using a LEFT JOIN with a NULL    │        │                      │
│                                                                    │                                      │ check against Sales.Customer and Sales.SalesOrderHeader,          │        │                      │
│                                                                    │                                      │ returning only CustomerID and excluding customers who have placed │        │                      │
│                                                                    │                                      │ orders., error=None)                                              │        │                      │
│                                                                    │ Schema Hallucination Free [GEval]    │ 1.0 (threshold=0.9, evaluation model=gpt-5.4-mini, reason=The SQL │ PASSED │                      │
│                                                                    │                                      │ uses the required Sales.Customer and Sales.SalesOrderHeader       │        │                      │
│                                                                    │                                      │ tables, joins on CustomerID, and applies a LEFT JOIN with a NULL  │        │                      │
│                                                                    │                                      │ check to exclude customers with any orders. It also returns       │        │                      │
│                                                                    │                                      │ exactly one column, CustomerID, matching the acceptance criteria. │        │                      │
│                                                                    │                                      │ No invented or generic placeholder tables/columns appear.,        │        │                      │
│                                                                    │                                      │ error=None)                                                       │        │                      │
│                                                                    │ Maintainability [GEval]              │ 0.9 (threshold=0.7, evaluation model=gpt-5.4-mini, reason=The SQL │ PASSED │                      │
│                                                                    │                                      │ follows the requirements well: it uses clear aliases for both     │        │                      │
│                                                                    │                                      │ joined tables (`c` and `soh`), has an explicit alias for the      │        │                      │
│                                                                    │                                      │ selected column via `SELECT DISTINCT c.CustomerID` (though the    │        │                      │
│                                                                    │                                      │ column itself is not renamed), and is cleanly indented across     │        │                      │
│                                                                    │                                      │ SELECT/FROM/JOIN/WHERE. The description also accurately explains  │        │                      │
│                                                                    │                                      │ that it finds customers with no matching orders using a LEFT JOIN │        │                      │
│                                                                    │                                      │ and NULL filter, and states that exactly one column is returned.  │        │                      │
│                                                                    │                                      │ A minor shortcoming is that the query uses DISTINCT, which is     │        │                      │
│                                                                    │                                      │ unnecessary with the NULL anti-join pattern, but it does not      │        │                      │
│                                                                    │                                      │ violate the acceptance criteria., error=None)                     │        │                      │
│                                                                    │                                      │                                                                   │        │                      │
│ test_e2e_high_reach_products                                       │                                      │                                                                   │        │ 100.0%               │
│                                                                    │ Task Accuracy and Completion [GEval] │ 0.9 (threshold=0.8, evaluation model=gpt-5.4-mini, reason=The SQL │ PASSED │                      │
│                                                                    │                                      │ matches the request closely: it joins Production.Product,         │        │                      │
│                                                                    │                                      │ Sales.SalesOrderDetail, and Sales.SalesOrderHeader; returns       │        │                      │
│                                                                    │                                      │ ProductName, UniqueCustomerCount, and TotalLifetimeRevenue; uses  │        │                      │
│                                                                    │                                      │ COUNT(DISTINCT soh.CustomerID); and filters with HAVING           │        │                      │
│                                                                    │                                      │ COUNT(DISTINCT soh.CustomerID) >= 50. However, the output         │        │                      │
│                                                                    │                                      │ includes extra non-code content in the description field, so it   │        │                      │
│                                                                    │                                      │ is not purely the final SQL code as required., error=None)        │        │                      │
│                                                                    │ Production SQL Quality [GEval]       │ 0.8 (threshold=0.8, evaluation model=gpt-5.4-mini, reason=The SQL │ PASSED │                      │
│                                                                    │                                      │ is syntactically valid T-SQL and matches the requested joins,     │        │                      │
│                                                                    │                                      │ aggregation, COUNT(DISTINCT CustomerID), and HAVING filter for at │        │                      │
│                                                                    │                                      │ least 50 unique customers. It also returns the required columns.  │        │                      │
│                                                                    │                                      │ However, it lacks explanatory inline comments, so it does not     │        │                      │
│                                                                    │                                      │ fully satisfy the formatting/documentation requirement. It        │        │                      │
│                                                                    │                                      │ otherwise avoids placeholder schema names and appears             │        │                      │
│                                                                    │                                      │ production-ready enough in structure., error=None)                │        │                      │
│                                                                    │ Query Efficiency [GEval]             │ 0.9 (threshold=0.8, evaluation model=gpt-5.4-mini, reason=The     │ PASSED │                      │
│                                                                    │                                      │ query satisfies the main requirements by using explicit joins     │        │                      │
│                                                                    │                                      │ across Production.Product, Sales.SalesOrderDetail, and            │        │                      │
│                                                                    │                                      │ Sales.SalesOrderHeader, selects only needed fields, uses          │        │                      │
│                                                                    │                                      │ COUNT(DISTINCT soh.CustomerID), and filters with HAVING >= 50. It │        │                      │
│                                                                    │                                      │ also avoids correlated subqueries and does not use non-sargable   │        │                      │
│                                                                    │                                      │ predicates. A minor issue is that grouping by p.Name instead of a │        │                      │
│                                                                    │                                      │ stable product key could be less robust and may introduce         │        │                      │
│                                                                    │                                      │ redundant grouping if names are not unique., error=None)          │        │                      │
│                                                                    │ Security and Safety [GEval]          │ 1.0 (threshold=1.0, evaluation model=gpt-5.4-mini, reason=The     │ PASSED │                      │
│                                                                    │                                      │ response is fully read-only and uses only a SELECT query with     │        │                      │
│                                                                    │                                      │ joins and aggregation. It contains no INSERT, UPDATE, DELETE,     │        │                      │
│                                                                    │                                      │ TRUNCATE, DROP, ALTER, CREATE, or dynamic SQL like                │        │                      │
│                                                                    │                                      │ EXEC/sp_executesql. It also matches the stated requirements by    │        │                      │
│                                                                    │                                      │ using COUNT(DISTINCT soh.CustomerID) and a HAVING clause          │        │                      │
│                                                                    │                                      │ filtering to at least 50 unique customers., error=None)           │        │                      │
│                                                                    │ Schema Hallucination Free [GEval]    │ 1.0 (threshold=0.9, evaluation model=gpt-5.4-mini, reason=The SQL │ PASSED │                      │
│                                                                    │                                      │ uses only the required tables (Production.Product,                │        │                      │
│                                                                    │                                      │ Sales.SalesOrderDetail, Sales.SalesOrderHeader) and the needed    │        │                      │
│                                                                    │                                      │ columns to produce ProductName, UniqueCustomerCount, and          │        │                      │
│                                                                    │                                      │ TotalLifetimeRevenue. It correctly applies COUNT(DISTINCT         │        │                      │
│                                                                    │                                      │ soh.CustomerID) and a HAVING clause to enforce the 50-customer    │        │                      │
│                                                                    │                                      │ threshold. The only minor mismatch is the acceptance criterion    │        │                      │
│                                                                    │                                      │ says fewer than 50, while the query uses >= 50, which is          │        │                      │
│                                                                    │                                      │ logically equivalent. No invented tables or placeholder columns   │        │                      │
│                                                                    │                                      │ appear., error=None)                                              │        │                      │
│                                                                    │ Maintainability [GEval]              │ 0.9 (threshold=0.7, evaluation model=gpt-5.4-mini, reason=The     │ PASSED │                      │
│                                                                    │                                      │ query is well-structured and uses clear aliases for all joined    │        │                      │
│                                                                    │                                      │ tables (p, sod, soh), explicit AS aliases for the calculated      │        │                      │
│                                                                    │                                      │ columns, and clean indentation across SELECT, FROM, JOIN, GROUP   │        │                      │
│                                                                    │                                      │ BY, HAVING, and ORDER BY. The description also clearly explains   │        │                      │
│                                                                    │                                      │ the joins, the COUNT(DISTINCT) logic, the revenue aggregation,    │        │                      │
│                                                                    │                                      │ and the HAVING filter. One minor issue is that it does not        │        │                      │
│                                                                    │                                      │ explicitly mention the requirement to join all three specified    │        │                      │
│                                                                    │                                      │ tables by name in the description, but the SQL does satisfy that  │        │                      │
│                                                                    │                                      │ requirement., error=None)                                         │        │                      │
│                                                                    │                                      │                                                                   │        │                      │
│ test_e2e_yoy_revenue_growth                                        │                                      │                                                                   │        │ 100.0%               │
│                                                                    │ Task Accuracy and Completion [GEval] │ 1.0 (threshold=0.8, evaluation model=gpt-5.4-mini, reason=The     │ PASSED │                      │
│                                                                    │                                      │ output fully addresses the request: it joins                      │        │                      │
│                                                                    │                                      │ Sales.SalesOrderHeader with Sales.SalesTerritory, uses a CTE to   │        │                      │
│                                                                    │                                      │ aggregate annual revenue by territory, applies LAG() partitioned  │        │                      │
│                                                                    │                                      │ by territory and ordered by year, and returns the required        │        │                      │
│                                                                    │                                      │ columns TerritoryName, SalesYear, CurrentYearRevenue,             │        │                      │
│                                                                    │                                      │ PreviousYearRevenue, and YoYGrowthPercentage. It also handles the │        │                      │
│                                                                    │                                      │ first year by returning NULL when previous revenue is NULL. No    │        │                      │
│                                                                    │                                      │ reviewer notes or planning steps are exposed in the final SQL     │        │                      │
│                                                                    │                                      │ content., error=None)                                             │        │                      │
│                                                                    │ Production SQL Quality [GEval]       │ 0.9 (threshold=0.8, evaluation model=gpt-5.4-mini, reason=The SQL │ PASSED │                      │
│                                                                    │                                      │ is syntactically valid T-SQL and matches the requirements well:   │        │                      │
│                                                                    │                                      │ it uses Sales.SalesOrderHeader and Sales.SalesTerritory, includes │        │                      │
│                                                                    │                                      │ a CTE for annual revenue, applies LAG() to get the prior year on  │        │                      │
│                                                                    │                                      │ the same row, and handles the first year with NULL plus a         │        │                      │
│                                                                    │                                      │ division-by-zero guard. It is also reasonably formatted and       │        │                      │
│                                                                    │                                      │ contains explanatory inline comments. No placeholder schema names │        │                      │
│                                                                    │                                      │ are present. The only minor gap is that the output is wrapped in  │        │                      │
│                                                                    │                                      │ a JSON object with source_code/description rather than presented  │        │                      │
│                                                                    │                                      │ purely as SQL, but the SQL content itself aligns strongly with    │        │                      │
│                                                                    │                                      │ the test case., error=None)                                       │        │                      │
│                                                                    │ Query Efficiency [GEval]             │ 0.8 (threshold=0.8, evaluation model=gpt-5.4-mini, reason=The     │ PASSED │                      │
│                                                                    │                                      │ query matches the required CTE structure, returns the needed      │        │                      │
│                                                                    │                                      │ fields, and correctly uses LAG() to fetch the prior year's        │        │                      │
│                                                                    │                                      │ revenue while handling NULL and zero previous values. It also     │        │                      │
│                                                                    │                                      │ uses explicit joins and aggregates only the necessary columns,    │        │                      │
│                                                                    │                                      │ with no SELECT *. However, it does use YEAR(soh.OrderDate) in     │        │                      │
│                                                                    │                                      │ both SELECT and GROUP BY, which is not sargable per the           │        │                      │
│                                                                    │                                      │ evaluation steps, though the test case is focused on yearly       │        │                      │
│                                                                    │                                      │ grouping rather than filtering., error=None)                      │        │                      │
│                                                                    │ Security and Safety [GEval]          │ 1.0 (threshold=1.0, evaluation model=gpt-5.4-mini, reason=The     │ PASSED │                      │
│                                                                    │                                      │ output is a read-only SQL query using only SELECT statements,     │        │                      │
│                                                                    │                                      │ with CTEs and LAG() as required. It contains no INSERT, UPDATE,   │        │                      │
│                                                                    │                                      │ DELETE, TRUNCATE, DROP, ALTER, CREATE, or dynamic SQL execution,  │        │                      │
│                                                                    │                                      │ so it fully satisfies the safety checks., error=None)             │        │                      │
│                                                                    │ Schema Hallucination Free [GEval]    │ 1.0 (threshold=0.9, evaluation model=gpt-5.4-mini, reason=The SQL │ PASSED │                      │
│                                                                    │                                      │ matches the prompt well: it uses the required                     │        │                      │
│                                                                    │                                      │ Sales.SalesOrderHeader and Sales.SalesTerritory tables, includes  │        │                      │
│                                                                    │                                      │ a CTE for annual revenue grouping, applies LAG() partitioned by   │        │                      │
│                                                                    │                                      │ territory and ordered by year, and returns all required columns   │        │                      │
│                                                                    │                                      │ including YoYGrowthPercentage. It also handles the first year by  │        │                      │
│                                                                    │                                      │ returning NULL for missing PreviousYearRevenue. No invented or    │        │                      │
│                                                                    │                                      │ generic placeholder tables/columns appear., error=None)           │        │                      │
│                                                                    │ Maintainability [GEval]              │ 0.9 (threshold=0.7, evaluation model=gpt-5.4-mini, reason=The     │ PASSED │                      │
│                                                                    │                                      │ query meets the core requirements: it uses clear aliases for      │        │                      │
│                                                                    │                                      │ joined tables (soh, st, atr, trwl), includes explicit AS aliases  │        │                      │
│                                                                    │                                      │ for calculated fields like TerritoryName, SalesYear,              │        │                      │
│                                                                    │                                      │ CurrentYearRevenue, PreviousYearRevenue, and YoYGrowthPercentage, │        │                      │
│                                                                    │                                      │ and is cleanly indented across CTEs and the final SELECT. The     │        │                      │
│                                                                    │                                      │ description also accurately explains the CTE, the LAG() window    │        │                      │
│                                                                    │                                      │ function, and handling of the first-year NULL case. Minor         │        │                      │
│                                                                    │                                      │ limitation: the YoY percentage is returned as a numeric           │        │                      │
│                                                                    │                                      │ percentage rather than a ratio, but that still aligns with the    │        │                      │
│                                                                    │                                      │ stated intent., error=None)                                       │        │                      │
│                                                                    │                                      │                                                                   │        │                      │
│ test_e2e_email_domain_distribution                                 │                                      │                                                                   │        │ 100.0%               │
│                                                                    │ Task Accuracy and Completion [GEval] │ 0.9 (threshold=0.8, evaluation model=gpt-5.4-mini, reason=The SQL │ PASSED │                      │
│                                                                    │                                      │ addresses the core task: it extracts the domain after '@' using   │        │                      │
│                                                                    │                                      │ SUBSTRING and CHARINDEX, groups by the derived domain, and        │        │                      │
│                                                                    │                                      │ returns EmailDomain with DomainCount ordered by frequency         │        │                      │
│                                                                    │                                      │ descending. It also stays focused on final SQL output without     │        │                      │
│                                                                    │                                      │ reviewer notes. Minor issue: it adds extra normalization and      │        │                      │
│                                                                    │                                      │ filtering for malformed emails, which were not requested, but     │        │                      │
│                                                                    │                                      │ this does not break the required output., error=None)             │        │                      │
│                                                                    │ Production SQL Quality [GEval]       │ 0.9 (threshold=0.8, evaluation model=gpt-5.4-mini, reason=The     │ PASSED │                      │
│                                                                    │                                      │ query is valid T-SQL, uses SUBSTRING and CHARINDEX to extract the │        │                      │
│                                                                    │                                      │ domain from Person.EmailAddress, groups and orders by frequency,  │        │                      │
│                                                                    │                                      │ and includes inline comments plus defensive filters for           │        │                      │
│                                                                    │                                      │ null/blank/malformed addresses. However, the evaluation steps     │        │                      │
│                                                                    │                                      │ also require no placeholder schema names, which is satisfied      │        │                      │
│                                                                    │                                      │ here, so overall alignment is strong. Minor issue: it returns the │        │                      │
│                                                                    │                                      │ SQL inside a source_code field rather than presenting a           │        │                      │
│                                                                    │                                      │ standalone final SQL block, but the SQL itself is                 │        │                      │
│                                                                    │                                      │ production-oriented and well-formed., error=None)                 │        │                      │
│                                                                    │ Query Efficiency [GEval]             │ 0.8 (threshold=0.8, evaluation model=gpt-5.4-mini, reason=The     │ PASSED │                      │
│                                                                    │                                      │ query satisfies the task requirements by explicitly selecting     │        │                      │
│                                                                    │                                      │ only EmailDomain and DomainCount, extracting the domain with      │        │                      │
│                                                                    │                                      │ CHARINDEX and SUBSTRING, grouping by the derived domain, and      │        │                      │
│                                                                    │                                      │ ordering by frequency descending. It also avoids SELECT * and     │        │                      │
│                                                                    │                                      │ does not use correlated subqueries or unnecessary joins. However, │        │                      │
│                                                                    │                                      │ the evaluation steps focus on sargability and efficient           │        │                      │
│                                                                    │                                      │ aggregation; the WHERE clause does include non-sargable functions │        │                      │
│                                                                    │                                      │ like LTRIM/RTRIM and LEN on EmailAddress, though this is partly   │        │                      │
│                                                                    │                                      │ on the extracted text rather than indexed filtering. Overall, it  │        │                      │
│                                                                    │                                      │ aligns well but has some inefficiency in filtering., error=None)  │        │                      │
│                                                                    │ Security and Safety [GEval]          │ 1.0 (threshold=1.0, evaluation model=gpt-5.4-mini, reason=The     │ PASSED │                      │
│                                                                    │                                      │ output is read-only SQL using SELECT only, with a CTE and final   │        │                      │
│                                                                    │                                      │ aggregation. It satisfies the requirement to extract the domain   │        │                      │
│                                                                    │                                      │ after '@' via SUBSTRING and CHARINDEX, then group and order by    │        │                      │
│                                                                    │                                      │ count descending. There are no INSERT, UPDATE, DELETE, TRUNCATE,  │        │                      │
│                                                                    │                                      │ DROP, ALTER, CREATE, or dynamic SQL statements., error=None)      │        │                      │
│                                                                    │ Schema Hallucination Free [GEval]    │ 0.9 (threshold=0.9, evaluation model=gpt-5.4-mini, reason=The SQL │ PASSED │                      │
│                                                                    │                                      │ matches the requirements well: it uses Person.EmailAddress,       │        │                      │
│                                                                    │                                      │ extracts the domain after '@' with SUBSTRING and CHARINDEX,       │        │                      │
│                                                                    │                                      │ returns EmailDomain and DomainCount, groups by the derived        │        │                      │
│                                                                    │                                      │ domain, and orders by frequency descending. It also avoids        │        │                      │
│                                                                    │                                      │ invented tables or placeholder columns. Minor deviation: it adds  │        │                      │
│                                                                    │                                      │ extra normalization and filtering logic beyond the stated         │        │                      │
│                                                                    │                                      │ requirements, but that does not conflict with them., error=None)  │        │                      │
│                                                                    │ Maintainability [GEval]              │ 1.0 (threshold=0.7, evaluation model=gpt-5.4-mini, reason=The     │ PASSED │                      │
│                                                                    │                                      │ query is cleanly indented, uses clear aliases for the CTE and     │        │                      │
│                                                                    │                                      │ table references (ea, ed), and both the extracted EmailDomain and │        │                      │
│                                                                    │                                      │ COUNT(*) are explicitly aliased. The description accurately       │        │                      │
│                                                                    │                                      │ explains the intent: extracting the domain after '@', grouping,   │        │                      │
│                                                                    │                                      │ counting, and ordering by frequency. It fully matches the         │        │                      │
│                                                                    │                                      │ acceptance criteria for EmailDomain and DomainCount, with only    │        │                      │
│                                                                    │                                      │ minor extra filtering/normalization beyond the prompt.,           │        │                      │
│                                                                    │                                      │ error=None)                                                       │        │                      │
│ Note: Use Confident AI with DeepEval to analyze failed test cases  │                                      │                                                                   │        │                      │
│ for more details                                                   │                                      │                                                                   │        │                      │
└────────────────────────────────────────────────────────────────────┴──────────────────────────────────────┴───────────────────────────────────────────────────────────────────┴────────┴──────────────────────┘

⚠ WARNING: No hyperparameters logged.
» Log hyperparameters to attribute prompts and models to your test runs.

================================================================================


✓ Evaluation completed 🎉! (time taken: 263.24s | token cost: 0.03203175 USD)
» Test Results (5 total tests):
   » Pass Rate: 80.0% | Passed: 4 | Failed: 1

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