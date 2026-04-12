# Домашнє завдання: MCP + ACP для мультиагентної системи (розширення hw8)

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

### Що змінилося порівняно з homework-8

| Було (homework-lesson-8) | Стало (homework-lesson-9) |
|-|-|
| Tools як Python-функції в одному процесі | Tools виставлені як MCP сервери (FastMCP) |
| Суб-агенти як `@tool`-обгортки для Supervisor | Суб-агенти доступні через ACP сервер (`acp-sdk`) |
| Все працює в одному процесі | Кожен MCP/ACP сервер — окремий HTTP endpoint |
| Прямий виклик функцій | Discovery → Delegate → Collect через протоколи |

### Приклад:

![Demo](/homework-lesson-9/gif%20example/agent_example.gif)

Приклади згенерованих звітів - в [output](/homework-lesson-9/output)

### Загальний опис

Агент запускається з терміналу (python3 main.py) та працює в інтерактивному режимі — користувач вводить запитання, отримує відповідь, і може продовжити діалог.
Агент підтримує зв'язний діалог — пам'ятає попередні повідомлення в межах сесії.

Для коректної роботи потрібен [API-ключ OpenAI](https://platform.openai.com/) та аналогічно для [Hugging Face](https://huggingface.co/settings/tokens), має бути створений файл .env з вказаними ключами: `OPENAI_API_KEY=<тут_ваш_ключ>` та `HF_TOKEN=<тут_ваш_ключ>`

Файл залежностей — [requirements.txt](https://github.com/viktor-taraba/MULTI-AGENT-SYSTEMS-course/blob/main/homework-lesson-9/requirements.txt), встановлення необхідних бібліотек `python3 -m pip install -r requirements.txt`

Підтримувані формати файлів для RAG (для збереження використовуєьтся chromadb):
- `PDF-файли (.pdf)` — спочатку намагаємося витягнути текст через `PyPDFLoader`. Якщо сторінки виявляються "порожніми" (наприклад, це скани або складний формат), використовуємо резервний `PyMuPDFLoader`.
- `Текстові файли (.txt)` — зчитуються як звичайний текст у кодуванні UTF-8 за допомогою `TextLoader`.
- `Markdown-файли (.md)` — також обробляються базовим TextLoader як звичайний текст.
- `Документи Microsoft Word (.docx)` — завантажуються за допомогою `Docx2txtLoader`
- `Субтитри YouTube-відео` — необхідний окремий файл `(.txt)` з переліком посилань (назва файлу задана у змінній `Youtube_links_file_name`), зчитаємо з нього посилання і отримуємо субтитри через `YoutubeLoader`, автоматично додаючи URL як джерело в метадані.

### Порядок запуску

```bash
# 1. Ingest documents for RAG (same as hw5/hw8)
python ingest.py

# 2. Start MCP servers (in separate terminals or as background processes)
python mcp_servers/search_mcp.py   # port 8901
python mcp_servers/report_mcp.py   # port 8902

# 3. Start ACP server
python acp_server.py               # port 8903

# 4. Run supervisor REPL
python main.py
```

### Опис інструментів для агентів:
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

MCP сервери для набору інструментів:

| MCP Server | Порт | Tools | Resources |
|:---|:---:|:---|:---|
| **SearchMCP** | 8901 | `web_search`, `read_url`, `knowledge_search` | `resource://knowledge-base-stats` — кількість документів, дата останнього оновлення |
| **ReportMCP** | 8902 | `save_report` | `resource://output-dir` — шлях до директорії та список збережених звітів |


### Архітектура

```
User (REPL)
  │
  ▼
Supervisor Agent (локальний, create_agent)
  │
  ├── delegate_to_planner(request)      ──► ACP ──► Planner Agent  ──► MCP ──► SearchMCP
  │                                                                             (web_search,
  │                                                                              knowledge_search)
  │
  ├── delegate_to_researcher(plan)      ──► ACP ──► Research Agent ──► MCP ──► SearchMCP
  │                                                                             (web_search,
  │                                                                              read_url,
  │                                                                              knowledge_search,
  |                                                                              find_articles_crossref,
  |                                                                              stock_company_info)
  │
  ├── delegate_to_critic(findings)      ──► ACP ──► Critic Agent   ──► MCP ──► SearchMCP
  │       │
  │       ├── verdict: "APPROVE" → go to save_report
  │       └── verdict: "REVISE"  → back to researcher with feedback
  │
  └── save_report(...)                  ──► MCP ──► ReportMCP
                                                     (save_report — HITL gated)
```

### Структура проєкту

```
homework-lesson-9/
├── main.py              # REPL with HITL interrupt/resume loop
├── supervisor.py        # Supervisor agent + ACP delegation tools
├── acp_server.py        # ACP server with 3 agents (planner, researcher, critic)
├── mcp_servers/
│   ├── search_mcp.py    # SearchMCP: web_search, read_url, knowledge_search, stock_company_info, find_articles_crossref
│   └── report_mcp.py    # ReportMCP: save_report
├── agents/
│   ├── planner.py       # Planner Agent definition
│   ├── research.py      # Research Agent definition
│   └── critic.py        # Critic Agent definition
├── schemas.py           # Pydantic models: ResearchPlan, CritiqueResult
├── mcp_utils.py         # mcp_tools_to_langchain helper
├── config.py            # Prompts + settings + ports
├── retriever.py         # Reused from hw5/hw8
├── ingest.py            # Reused from hw5/hw8
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
│   └── pbir_multi_agent_tools_report           # Example generated report (#4)
│   └── bm25_vs_tfidf_report                    # Example generated report (#5)
└── README.md            # Setup instructions, architecture overview
```

Приклад консольного виводу (фрагмент):

```
Research Agent
type 'exit' or 'quit' to quit
----------------------------------------------------------------------------------------------------

You: PBIR structure (new format for Power BI reports)

🤖 Agent:
I can do that — before I start: do you want a technical specification (file/JSON schema, field definitions, example PBIR files and how to generate/validate them) or a high-level overview (purpose, components, and migration guidance)?

You: high-level overview
🔧 Tool called -> plan({'request': 'Provide a high-level overview of PBIR structure (new format for Power BI reports). The ...)

╭──────────────────────────────
│   [Supervisor → ACP → Planner]
╰──────────────────────────────
    🔧 Tool called -> web_search({'query': 'PBIR file format Power BI', 'max_search_results': 4})
    ✅ Result (web_search): [{"title": "Power BI enhanced report format (PBIR) in Power BI Desktop", "url": "https://powerbi.mic...
✅ Result (plan):

╭─── 📄 Plan ────────────────────────────────────
│ {
│   "goal": "Create a concise, actionable high-level overview of the PBIR (Power BI enhanced report) structure for BI architects and report authors — covering purpose, components, file organization, key metadata fields, comparison to earlier Power BI formats (PBIX/PBIP), migration guidance, best practices, and security/validation considerations.",
│   "search_queries": [
│     "Power BI PBIR file format specification Microsoft blog \"PBIR\" \"Power BI enhanced report format\"",
│     "PBIR vs PBIX vs PBIP differences \"PBIR will become the default\"",
│     "PBIR file structure manifest metadata fields \"PBIR\" \"manifest\"",
│     "Power BI PBIR migration guide \"migrate PBIX to PBIR\"",
│     "Power BI PBIR security signing encryption validation \"PBIR\"",
│     "Power BI Desktop developer mode PBIR developer preview release notes",
│     "example PBIR file tree directory layout \"PBIR\" sample structure",
│     "best practices PBIR report authors \"Power BI\""
│   ],
│   "sources_to_check": [
│     "web_search",
│     "read_url",
│     "knowledge_search"
│   ],
│   "output_format": "A concise Markdown report for BI architects and report authors with these sections: 1) Executive summary (1 paragraph); 2) Purpose (1 short paragraph); 3) Components (bulleted list with 1-line descriptions for each component/file); 4) File organization (sample directory/tree code block + short explanation of each folder/file); 5) Key metadata fields (compact table: field name | type | purpose | required/optional); 6) Comparison to previous formats (2-column table: PBIR vs PBIX/PBIP highlighting key differences and impact areas); 7) Migration guidance (practical step-by-step checklist, common pitfalls, validation steps, estimated effort for typical reports); 8) Best practices (8–12 concise bullets for architects/report authors); 9) Security & validation considerations (checklist, tools, signing/permissions notes); 10) References & links (3–6 authoritative links) — prioritize clarity, actionable bullets, sample manifest snippets and a sample validation checklist. Final deliverable: a well-formatted, visually clear Markdown document suitable for immediate distribution to BI teams."
│ }
╰──────────────────────────────────────────────

🔧 Tool called -> research({'plan': 'Execute this research plan: Create a concise, actionable high-level Markdown report for BI...)

╭──────────────────────────────
│   [Supervisor → ACP → Researcher]
╰──────────────────────────────
    🔧 Tool called -> web_search({'query': 'PBIR Power BI enhanced report PBIR format PBIP PBIX Microsoft docs', 'max_search_results'...)
    ✅ Result (web_search): [{"title": "Create a Power BI report in enhanced report format - Power BI", "url": "https://learn.mi...
    🔧 Tool called -> knowledge_search({'query': 'PBIR enhanced report format PBIP PBIX'})
    ✅ Result (knowledge_search): --- Document 1 ---
Source: PBIR Format Reference.md (Page: Unknown)
Content:
- **Check examples:** C...
    🔧 Tool called -> web_search({'query': 'Power BI enhanced report format manifest example PBIR manifest sample "manifest.json" PBI...)
    ✅ Result (web_search): [{"title": "Paginated Report Recipes eBook \u2013 Paul Turley's SQL", "url": "https://sqlserverbi.bl...
    🔧 Tool called -> read_url({'url': 'https://learn.microsoft.com/en-us/power-bi/developer/embedded/projects-enhanced-report-form...)
    ✅ Result (read_url): Note
Access to this page requires authorization. You can try signing in or changing directories.
Acc...
    🔧 Tool called -> read_url({'url': 'https://powerbi.microsoft.com/en-us/blog/power-bi-enhanced-report-format-pbir-in-power-bi-d...)
    ✅ Result (read_url): Enhancing team collaboration and automation is crucial for any enterprise BI development, which is t...
...
```
