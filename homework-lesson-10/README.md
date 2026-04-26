# Домашнє завдання: тестування мультиагентної системи (розширення hw8)

![OpenAI](https://img.shields.io/badge/OpenAI-API-black.svg)
![langchain](https://img.shields.io/badge/langchain-1.2.0+-orange.svg)
![langgraph](https://img.shields.io/badge/langgraph-1.1.2+-orange.svg)
![yfinance](https://img.shields.io/badge/yfinance-1.2.0+-orange.svg)
![trafilatura](https://img.shields.io/badge/trafilatura-2.0.0+-orange.svg)
![pypdf](https://img.shields.io/badge/pypdf-6.9.1+-orange.svg)
![pandas](https://img.shields.io/badge/pandas-3.0.1+-orange.svg)
![ddgs](https://img.shields.io/badge/ddgs-9.11.4+-orange.svg)
![requests](https://img.shields.io/badge/requests-2.32.5+-orange.svg)
![chromadb](https://img.shields.io/badge/chromadb-1.5.5+-orange.svg)
![youtube-transcript-api](https://img.shields.io/badge/youtube--transcript--api-1.2.4+-orange.svg)
![transformers](https://img.shields.io/badge/transformers-5.4.0+-orange.svg)
![docx2txt](https://img.shields.io/badge/docx2txt-0.9+-orange.svg)
![rank_bm25](https://img.shields.io/badge/rank_bm25-0.2.2+-orange.svg)

### Що змінюється порівняно з homework-8

| Було (homework-lesson-8) | Стало (homework-lesson-10)                    |
|-|----------------------------------------------|
| Мультиагентна система без тестів | Та сама система + покриття тестами           |
| Якість перевіряється вручну (vibe check) | Автоматизовані evals з метриками 0–1         |
| Немає golden dataset | 12 golden examples (happy path + edge cases + failure cases) для regression testing |
| Немає CI-ready тестів | запуск тестів через pytest |

### Тести

|Назва тесту|Якого агента тестуємо|Що перевіряємо|
|--|--|--|
|test_plan_quality|Planner|Структуру та якість плану|
|test_plan_has_queries|Planner|Наявність пошукових запитів в search_queries та їх релевантність|
|test_query_diversity|Planner|Широта та повнота покриття питання запитами|
|test_research_grounded|Researcher|groundedness відповіді (звіту)|
|test_research_edge_case|Researcher|Hallucination - перевірка на прикладі неіснуючої експедиції|
|test_critique_approve|Critic|Структуру та обгрунтування критики на прикладі якісно підготовленого звіту|
|test_critique_revise|Critic|Структуру та обгрунтування критики на прикладі погано підготовленого звіту|
|test_planner_tools|Planner|Tool Correctness - Використання тулів web_search та knowledge_search для пошуку інформації|
|test_researcher_tools|Researcher|Tool Correctness - Використання тулів web_search, knowledge_search, knowledge_search для пошуку|
|test_critic_tools|Critic|Tool Correctness - Використання тулів web_search та read_url для верифікації звіту|
|test_supervisor_save|Supervisor|Tool Correctness - Використання save_report після approve від критика|

Використовую pytest напряму замість deepeval через обмеження з боку  Application Control (Windows App Control and Smart App Control) `Program 'deepeval.exe' failed to run: An Application Control policy has blocked this file` 

#### 4. End-to-end тест

Протестуйте повний pipeline Supervisor → Planner → Researcher → Critic:

```python
answer_relevancy = AnswerRelevancyMetric(threshold=0.7, model="gpt-5.4-mini")

correctness = GEval(
    name="Correctness",
    evaluation_steps=[
        "Check whether the facts in 'actual output' contradict 'expected output'",
        "Penalize omission of critical details",
        "Different wording of the same concept is acceptable",
    ],
    evaluation_params=[
        LLMTestCaseParams.INPUT,
        LLMTestCaseParams.ACTUAL_OUTPUT,
        LLMTestCaseParams.EXPECTED_OUTPUT,
    ],
    model="gpt-5.4-mini",
    threshold=0.6,
)
```

### Загальний опис

Агент запускається з терміналу (python3 main.py) та працює в інтерактивному режимі — користувач вводить запитання, отримує відповідь, і може продовжити діалог.
Агент підтримує зв'язний діалог — пам'ятає попередні повідомлення в межах сесії.

Для коректної роботи потрібен [API-ключ OpenAI](https://platform.openai.com/) та аналогічно для [Hugging Face](https://huggingface.co/settings/tokens), має бути створений файл .env з вказаними ключами: `OPENAI_API_KEY=<тут_ваш_ключ>` та `HF_TOKEN=<тут_ваш_ключ>`

Файл залежностей — [requirements.txt](https://github.com/viktor-taraba/MULTI-AGENT-SYSTEMS-course/blob/main/homework-lesson-8/requirements.txt), встановлення необхідних бібліотек `python3 -m pip install -r requirements.txt`

Підтримувані формати файлів для RAG (для збереження використовуєьтся chromadb):
- `PDF-файли (.pdf)` — спочатку намагаємося витягнути текст через `PyPDFLoader`. Якщо сторінки виявляються "порожніми" (наприклад, це скани або складний формат), використовуємо резервний `PyMuPDFLoader`.
- `Текстові файли (.txt)` — зчитуються як звичайний текст у кодуванні UTF-8 за допомогою `TextLoader`.
- `Markdown-файли (.md)` — також обробляються базовим TextLoader як звичайний текст.
- `Документи Microsoft Word (.docx)` — завантажуються за допомогою `Docx2txtLoader`
- `Субтитри YouTube-відео` — необхідний окремий файл `(.txt)` з переліком посилань (назва файлу задана у змінній `Youtube_links_file_name`), зчитаємо з нього посилання і отримуємо субтитри через `YoutubeLoader`, автоматично додаючи URL як джерело в метадані.

### Опис тулів для агентів:
|Назва|Параметри|Опис|
|--|--|--|
|`web_search`|`query: str`|Шукає актуальну інформацію в інтернеті через DuckDuckGo. Повертає перелік знайдених посилань з даними про заголовок, URL, фрагмент тексту. Використовується як перший крок пошуку.|
|`read_url`|`url: str`|Отримує основний текст із вебсторінки (або PDF, якщо це пряме посилання на pdf-звіт чи статтю).|
|`stock_company_info`|`stock_ticker: str, result_type: str`|Отримує фінансові дані або загальний профіль компанії через Yahoo Finance API.|
|`find_articles_crossref`|`query: str`|Шукає наукові статті в базі Crossref. Повертає відфільтрований список записів із валідною анотацією (назва, анотація, DOI, рік).|
|`knowledge_search`|`query: str`|Пошук у локальній базі знань за допомогою гібридного пошуку (hybrid retrieval) та реранкінгу.|
|`write_report`|`filename: str, content: str`|Зберігає фінальний звіт у форматі Markdown, використовується як останній крок для видачі результату.|
|`plan`|`request: str`|Субагент Planner (агент як tool для Supervisor)|
|`research`|`plan: str`|Субагент Research (агент як tool для Supervisor)|
|`critique`|`findings: str`|Субагент Research (агент як tool для Supervisor)|

### Архітектура

```
User (REPL)
  │
  ▼
Supervisor Agent
  │
  ├── 1. plan(request)       → Planner Agent      → [web_search, knowledge_search]  → structured ResearchPlan
  │
  ├── 2. research(plan)      → Research Agent     → [web_search, read_url, knowledge_search, stock_company_info, find_articles_crossref]   → structured ResearchResult
  │
  ├── 3. critique(findings)  → Critic Agent       → [web_search, read_url, knowledge_search, stock_company_info, find_articles_crossref]   → structured CritiqueResult
  │       │
  │       ├── verdict: "APPROVE"  → go to step 4
  │       └── verdict: "REVISE"   → back to step 2 with feedback
  │
  └── 4. write_report(...)   → save_report tool   → HITL gated
```

### Структура проєкту

```
homework-lesson-8/
├── tests/
│   ├── golden_dataset.json       # 15-20 golden examples
│   ├── test_planner.py           # Planner agent tests
│   ├── test_researcher.py        # Research agent tests (groundedness)
│   ├── test_critic.py            # Critic agent tests
│   ├── test_tools.py             # Tool correctness tests
│   └── test_e2e.py               # End-to-end evaluation on golden dataset
├── main.py              # REPL with HITL interrupt/resume loop
├── supervisor.py        # Supervisor agent + agent-as-tool wrappers
├── agents/
│   ├── planner.py       # Planner Agent (uses ResearchPlan from schemas.py)
│   ├── research.py      # Research Agent (reuses hw5 tools)
│   └── critic.py        # Critic Agent (uses CritiqueResult from schemas.py)
├── schemas.py           # Pydantic models: ResearchPlan, CritiqueResult
├── tools.py             # Reused from hw5: web_search, read_url, knowledge_search, stock_company_info, find_articles_crossref + save_report
├── retriever.py         # Reused from hw5
├── ingest.py            # Reused from hw5
├── config.py            # Prompts + settings
├── requirements.txt     # Dependencies (add langgraph to hw5 deps)
├── data/                # Documents for RAG (from hw5)
├── chunks/              # Результат роботи ingestion.py (JSON файл зі збереженими чанками)
│   └── bm25_chunks.json         # JSON файл зі збереженими чанками
├── index/               # Векторна БД
│   └──... (.bin, .pickle, .sqlite3 files)
├── gif example/         # Приклад роботи агента
│   └── agent_example.gif
├── .env                 # API ключі
├── output/
│   └── dividend_policy_factors_report.md       # Example generated report (#1)
│   └── pbir_multi_agent_prompting_report.md    # Example generated report (#2)
│   └── pbir_tmdl_validator_report.md           # Example generated report (#3)
└── README.md            # Setup instructions, architecture overview
```

### Структура проєкту

```
homework-lesson-10/
├── tests/
│   ├── golden_dataset.json       # 15-20 golden examples
│   ├── test_planner.py           # Planner agent tests
│   ├── test_researcher.py        # Research agent tests (groundedness)
│   ├── test_critic.py            # Critic agent tests
│   ├── test_tools.py             # Tool correctness tests
│   └── test_e2e.py               # End-to-end evaluation on golden dataset
├── ... (all files from homework-lesson-8)
└── README.md
```

### Як запустити тести

```bash
# Run all tests
deepeval test run tests/

# Run specific test file
deepeval test run tests/test_planner.py

# Run with verbose output
deepeval test run tests/ -v
```

Приклад запуску:
```
PS C:\Users\Viktor> cd C:\Users\Viktor\source\repos\MULTI-AGENT-SYSTEMS-course\homework-lesson-10
PS C:\Users\Viktor\source\repos\MULTI-AGENT-SYSTEMS-course\homework-lesson-10> python -m pytest tests/test_tools.py -v -s --tb=short -W ignore::DeprecationWarning --show-capture=no --no-header
================================================= test session starts =================================================
collected 4 items


✅ test_planner_tools (ToolCorrectnessMetric: 1.0, threshold: 0.7)
PASSED

✅ test_researcher_tools (ToolCorrectnessMetric: 1.0, threshold: 0.7)
PASSED

✅ test_critic_tools (ToolCorrectnessMetric: 1.0, threshold: 0.7)
PASSED

✅ test_supervisor_save (ToolCorrectnessMetric: 1.0, threshold: 0.7)
PASSEDRunning teardown with pytest sessionfinish...


======================================================================================== 4 passed in 421.79s (0:07:01) =========================================================================================
PS C:\Users\Viktor\source\repos\MULTI-AGENT-SYSTEMS-course\homework-lesson-10> python -m pytest tests/test_critic.py -v -s --tb=short -W ignore::DeprecationWarning --show-capture=no --no-header
============================================================================================= test session starts ==============================================================================================
collected 2 items


✅ test_critique_approve (Critique Quality: 0.8, threshold: 0.7)
PASSED

✅ test_critique_revise (Critique Quality: 0.8, threshold: 0.7)
PASSEDRunning teardown with pytest sessionfinish...


======================================================================================== 2 passed in 215.82s (0:03:35) =========================================================================================
PS C:\Users\Viktor\source\repos\MULTI-AGENT-SYSTEMS-course\homework-lesson-10> python -m pytest tests/test_researcher.py -v -s --tb=short -W ignore::DeprecationWarning --show-capture=no --no-header
============================================================================================= test session starts ==============================================================================================
collected 2 items


✅ test_research_grounded (Groundedness: 0.7, threshold: 0.7)
PASSED

❌ test_research_edge_case (No Hallucination: 0.0, threshold: 0.8)
   Reason: The output does not say that no credible information could be found; instead it gives a long, confident report with many concrete claims about penguin biogeography, adaptations, field methods, and named organizations. Although it is polite and objective, it clearly invents or asserts scientific and logistical details for a fictional expedition rather than refusing to hallucinate.
FAILEDRunning teardown with pytest sessionfinish...


=================================================================================================== FAILURES ===================================================================================================
___________________________________________________________________________________________ test_research_edge_case ____________________________________________________________________________________________
tests\test_researcher.py:68: in test_research_edge_case
    evaluate_and_assert(edge_case_fictional, "test_research_edge_case", "edge_case_fictional")
tests\helper.py:31: in evaluate_and_assert
    pytest.fail(f"DeepEval {threshold_name} threshold not met.")
E   Failed: DeepEval edge_case_fictional threshold not met.
=========================================================================================== short test summary info ============================================================================================
FAILED tests/test_researcher.py::test_research_edge_case - Failed: DeepEval edge_case_fictional threshold not met.
=================================================================================== 1 failed, 1 passed in 303.11s (0:05:03) ====================================================================================
PS C:\Users\Viktor\source\repos\MULTI-AGENT-SYSTEMS-course\homework-lesson-10> python -m pytest tests/test_planner.py -v -s --tb=short -W ignore::DeprecationWarning --no-header
============================================================================================= test session starts ==============================================================================================
collected 3 items


✅ test_plan_quality (Plan Quality: 0.9, threshold: 0.7)
PASSED

✅ test_plan_has_queries (Plan Quality: 0.9, threshold: 0.7)
PASSED

✅ test_query_diversity (Query Diversity: 0.8, threshold: 0.75)
PASSEDRunning teardown with pytest sessionfinish...


======================================================================================== 3 passed in 203.07s (0:03:23) =========================================================================================
```
