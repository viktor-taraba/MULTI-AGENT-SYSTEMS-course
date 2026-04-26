# Домашнє завдання: Langfuse observability

![OpenAI](https://img.shields.io/badge/OpenAI-API-black.svg)
![langchain](https://img.shields.io/badge/langchain-1.2.0-orange.svg)
![langgraph](https://img.shields.io/badge/langgraph-1.1.2-orange.svg)
![yfinance](https://img.shields.io/badge/yfinance-1.2.0-orange.svg)
![trafilatura](https://img.shields.io/badge/trafilatura-2.0.0-orange.svg)
![pypdf](https://img.shields.io/badge/pypdf-6.9.1-orange.svg)
![pandas](https://img.shields.io/badge/pandas-3.0.1-orange.svg)
![ddgs](https://img.shields.io/badge/ddgs-9.11.4-orange.svg)
![requests](https://img.shields.io/badge/requests-2.32.5-orange.svg)
![chromadb](https://img.shields.io/badge/chromadb-1.5.5-orange.svg)
![youtube-transcript-api](https://img.shields.io/badge/youtube--transcript--api-1.2.4+-orange.svg)
![transformers](https://img.shields.io/badge/transformers-5.4.0-orange.svg)
![docx2txt](https://img.shields.io/badge/docx2txt-0.9-orange.svg)
![rank_bm25](https://img.shields.io/badge/rank_bm25-0.2.2-orange.svg)
![deepeval](https://img.shields.io/badge/deepeval-3.9.7-orange.svg)
![langfuse](https://img.shields.io/badge/langfuse-4.5.1-orange.svg)

### Що змінилося порівняно з попередніми homework

| Було | Стало |
|---|---|
| Немає observability — система працює як чорна скринька | Кожен запуск трейситься в Langfuse з повним деревом викликів |
| DeepEval тести запускаються локально вручну (hw10) | Langfuse автоматично оцінює нові трейси через LLM-as-a-Judge |
| Промпти захардкоджені в коді | Усі system prompts агентів винесено в Langfuse Prompt Management |

### Скріншоти з Langfuse UI

#### Sessions
![sessions](/homework-lesson-12/screenshots/sessions.png)

#### Trace tree / tracing
![tracing_1](/homework-lesson-12/screenshots/tracing_1.png)
![tracing_2](/homework-lesson-12/screenshots/tracing_2.png)
![tracing_3](/homework-lesson-12/screenshots/tracing_3.png)

#### Evaluator scores / LLM-as-a-Judge
![llm_as_a_judge_1](/homework-lesson-12/screenshots/llm_as_a_judge_1.png)
![llm_as_a_judge_2](/homework-lesson-12/screenshots/llm_as_a_judge_2.png)
![llm_as_a_judge_3](/homework-lesson-12/screenshots/llm_as_a_judge_3.png)
![scores_dashboard](/homework-lesson-12/screenshots/scores_dashboard.png)

#### Prompt management
![prompts](/homework-lesson-12/screenshots/prompts.png)

### Загальний опис

Агент запускається з терміналу (python3 main.py) та працює в інтерактивному режимі — користувач вводить запитання, отримує відповідь, і може продовжити діалог.
Агент підтримує зв'язний діалог — пам'ятає попередні повідомлення в межах сесії. Приклади згенерованих звітів - в [output](/homework-lesson-12/output)

Для коректної роботи потрібен [API-ключ OpenAI](https://platform.openai.com/) та аналогічно для [Hugging Face](https://huggingface.co/settings/tokens) та [Langfuse](https://us.cloud.langfuse.com/) (`LANGFUSE_PUBLIC_KEY`,`LANGFUSE_SECRET_KEY`,`LANGFUSE_BASE_URL`), має бути створений файл .env з вказаними ключами: `OPENAI_API_KEY=<тут_ваш_ключ>` та `HF_TOKEN=<тут_ваш_ключ>`

Файл залежностей — [requirements.txt](https://github.com/viktor-taraba/MULTI-AGENT-SYSTEMS-course/blob/main/homework-lesson-12/requirements.txt), встановлення необхідних бібліотек `python3 -m pip install -r requirements.txt`

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
│   ├── golden_dataset.json             # 12 golden examples
│   ├── test_planner.py                 # Planner agent tests
│   ├── test_researcher.py              # Research agent tests
│   ├── test_critic.py                  # Critic agent tests
│   ├── test_tools.py                   # Tool correctness tests
│   ├── test_e2e.py                     # End-to-end evaluation on golden dataset
│   ├── helper.py                       # Helper functions for tests
│   ├── test_e2e_generate               # perparation for test_e2e (generating outputs for golden examples to be used as references in test_e2e)
│   ├── e2e_results/
│   |   └── generated_responses.json    # Responses generated by test_e2e_generate for golden examples (used in test_e2e)
│   └── critic_tests_examples/          # Examples used in test_critic.py for approve/revise cases
│       ├── ponziani_opening_report.md
│       └── pbir_multi_agent_prompting_report.md 
├── main.py              # REPL with HITL interrupt/resume loop
├── supervisor.py        # Supervisor agent + agent-as-tool wrappers
├── agents/
│   ├── planner.py       # Planner Agent (uses ResearchPlan from schemas.py)
│   ├── research.py      # Research Agent
│   └── critic.py        # Critic Agent (uses CritiqueResult from schemas.py)
├── screenshots/
│   └── ...				 # Langfuse UI screenshots
├── schemas.py           # Pydantic models: ResearchPlan, CritiqueResult
├── tools.py             # Reused from hw8: web_search, read_url, knowledge_search, stock_company_info, find_articles_crossref + save_report
├── retriever.py         # Reused from hw8
├── ingest.py            # Reused from hw8
├── config.py            # settings
├── requirements.txt     # Dependencies
├── data/                # Documents for RAG (from hw8)
├── chunks/              # Результат роботи ingestion.py (JSON файл зі збереженими чанками)
│   └── bm25_chunks.json         # JSON файл зі збереженими чанками
├── index/               # Векторна БД
│   └──... (.bin, .pickle, .sqlite3 files)
├── gif example/         # Приклад роботи агента
│   └── agent_example.gif
├── .env                 # API ключі
├── output/
│   └── ...				 # Examples (generated .md reports)
└── README.md            # Setup instructions, architecture overview
```