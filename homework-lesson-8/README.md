# Завдання: мультиагентна дослідницька система (розширення hw5)

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

### Що змінилося порівняно з homework-5

| Було (homework-lesson-5) | Стає (homework-lesson-8) |
|-|-|
| Один Research Agent | Supervisor + 3 суб-агенти |
| Агент робить усе одразу | Planner досліджує домен і декомпозує задачу, Researcher виконує, Critic перевіряє |
| Одноразове дослідження | Ітеративне: Critic може повернути Researcher на доопрацювання |
| Без потоку затвердження | HITL: операції запису потребують підтвердження користувача |
| Лише вільний текст | Planner і Critic повертають структурований вивід (Pydantic) |

### Приклад:

![Demo](/homework-lesson-8/gif%20example/agent_example.gif)

Приклади згенерованих звітів - в [output](/homework-lesson-8/output)

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

Приклад консольного виводу (фрагмент):

```
Research Agent
type 'exit' or 'quit' to quit
----------------------------------------------------------------------------------------------------

You: Фактори, що впливають на дивідендну політику компанії
🔧 Tool called -> plan({'request': 'Фактори, що впливають на дивідендну політику компанії — створити план дослідження. Вклю...)

╭──────────────────────────────
│   [Supervisor → Planner]
╰──────────────────────────────
    🔧 Tool called -> web_search({'query': 'factors affecting dividend policy academic literature determinants of dividends empirical...)
    🔧 Tool called -> web_search({'query': 'signaling theory dividends empirical evidence study 2010 2020 signalling dividends resear...)
    🔧 Tool called -> web_search({'query': 'residual dividend theory explanation and empirical tests'})
    🔧 Tool called -> web_search({'query': 'bird-in-hand theory dividends empirical evidence Jensen Miller Modigliani 1961 critique'})
    🔧 Tool called -> web_search({'query': 'dividend policy determinants cross-country study emerging markets Ukraine dividends resea...)
    🔧 Tool called -> web_search({'query': 'Ukrainian companies dividend policy examples 2020 2023 PrivatBank Ukrnafta Kernel dividen...)
    🔧 Tool called -> web_search({'query': 'agency theory and dividends empirical evidence payout policy as mitigation tool'})
    🔧 Tool called -> web_search({'query': 'taxation impact on dividend policy empirical study corporate taxes dividends'})
    🔧 Tool called -> web_search({'query': 'practical recommendations for corporate dividend policy managers best practices white pap...)
    🔧 Tool called -> web_search({'query': "recommended sources academic books corporate finance dividend policy Lintner 'dividend po...)
    ✅ Result (web_search): [{"title": "Determinants of Dividend Payout Policy: More Evidence From ...", "url": "https://onlinel...
    ✅ Result (web_search): [{"title": "Dividend Policy: A Review of Theories and Empirical Evidence", "url": "https://www.resea...
    ✅ Result (web_search): [{"title": "Dividend policy - Wikipedia", "url": "https://en.wikipedia.org/wiki/Dividend_policy", "s...
    ✅ Result (web_search): [{"title": "PDFAnalysis Of Dividend Policies, Theories, And Models", "url": "https://www.seahipublic...
    ✅ Result (web_search): [{"title": "Impact of Taxation on Dividend Policy | UKDiss.com", "url": "https://ukdiss.com/intro/th...
    ✅ Result (web_search): [{"title": "Imperfect information, dividend policy, and \"the bird in the hand\" fallacy", "url": "h...
    ✅ Result (web_search): [{"title": "Dividend Payments Complete for 2023 | Ukrnafta", "url": "https://www.ukrnafta.com/en/div...
    ✅ Result (web_search): [{"title": "Lintner's model of dividend payments - Macquarie UniversityTHE LINTNER MODEL AND DIVIDEN...
    ✅ Result (web_search): [{"title": "A Systematic Literature Review of Factors Influencing the Dividend Policy", "url": "http...
    ✅ Result (web_search): [{"title": "Efficient-market hypothesis - Wikipedia", "url": "https://en.wikipedia.org/wiki/Efficien...
✅ Result (plan):

╭─── 📄 Plan ────────────────────────────────────
│ {
│   "goal": "Підготувати структурований план дослідження на тему «Фактори, що впливають на дивідендну політику компанії», який охоплює: ключові внутрішні та зовнішні фактори, теоретичні моделі (signaling, residual, bird‑in‑hand, Lintner тощо), емпіричні докази, приклади (міжнародні та українські), практичні рекомендації для менеджменту, конкретні пошукові запити та рекомендовані джерела; а також визначити структуру фінального звіту у форматі Markdown і формат цитування.",
│   "search_queries": [
│     "factors affecting dividend policy determinants of dividends empirical review 2015..2025",
│     "dividend signaling theory empirical evidence meta-analysis Bhattacharya 1979 signalling dividends",
│     "residual dividend theory empirical tests 'residual dividend' study",
│     "bird-in-hand theory Gordon Lintner empirical evidence 'bird in the hand' dividends",
│     "Lintner model dividend partial adjustment tests emerging markets 'Lintner 1956'",
│     "agency theory dividends 'dividends agency costs' empirical evidence",
│     "taxation effect on dividend policy 'dividend taxes' corporate behavior 2003 tax cut NBER",
│     "dividend policy determinants emerging markets panel data 'payout ratio' 'free cash flow' 'leverage' 'growth opportunities'",
│     "dividend policy Ukraine case study Ukrnafta Kernel 'dividend payments 2023' 'investor relations'",
│     "country risk geopolitical risk effect on dividends 'geopolitical risk' dividend policy emerging markets",
│     "dividend smoothing and ownership structure 'foreign ownership' dividends emerging markets",
│     "practical corporate guidelines dividend policy 'dividend policy best practices' white paper 'investor relations'",
│     "major literature reviews dividend policy 'bibliometric review' 'systematic literature review' 2020..2024",
│     "datasets for dividend research 'Compustat' 'Orbis' 'Worldscope' Ukraine listed firms financials"
│   ],
│   "sources_to_check": [
│     "web_search (Google Scholar, SSRN, JSTOR, ScienceDirect, Wiley Online Library, NBER, ResearchGate)",
│     "Google Scholar searches and export of key PDFs",
│     "Company investor-relations pages (Ukrnafta, Kernel, Naftogaz, PrivatBank, major international firms) via corporate websites",
│     "Ukrainian regulators and institutions: National Securities and Stock Market Commission of Ukraine, Ministry of Finance of Ukraine, Ukrainian Exchange (UX) publications and reports",
│     "International institutions: World Bank, IMF country reports (Ukraine), OECD corporate governance working papers",
│     "Major academic sources and classic papers: Miller & Modigliani (1961), Lintner (1956), Gordon (1959), Bhattacharya (1979), Jensen & Meckling (1976) — locate via JSTOR/NBER",
│     "Recent empirical papers and reviews: 'A bibliometric review of dividend policy literature' (2023), 'Determinants of Dividend Payout Policy: More Evidence From Emerging Markets' (2024), and NBER/CEPR working papers on dividend taxation",
│     "Databases for firm-level data: Compustat, Worldscope/Orbis, Bloomberg, Refinitiv Eikon — and local sources for Ukrainian firms' financial statements",
│     "Worked examples and case notes from business schools (NYU Stern/Aswath Damodaran notes on chapter about dividends)"
│   ],
│   "output_format": "Формат та план фінального звіту (Markdown). Фінальний документ — звіт у Markdown, візуально привабливий, ~20–40 сторінок еквіваленту. Формат цитування: APA 7th edition. Приклади цитат: стаття — (Автор, рік); книга — Автор (рік); веб-сторінка — Автор/Організація (рік). Структура звіту та покроковий план дослідження (не більше 15 кроків):\n\n1) Титул і метадані — назва, автор, дата, коротка інструкція для читача.\n2) Виконавче резюме (2 абзаци) — основні висновки і рекомендації для менеджменту.\n3) Зміст.\n4) Вступ — мета дослідження, питання, обмеження, методологія пошуку (ключові запити, критерії включення/виключення).\n5) Теоретична частина — короткі ..."
│ }
╰──────────────────────────────────────────────

🔧 Tool called -> research({'plan': 'Execute this research plan: Goal: Prepare a comprehensive Markdown report on "Factors affe...)

╭──────────────────────────────
│   [Supervisor → Researcher]
╰──────────────────────────────
    🔧 Tool called -> web_search({'query': 'Lintner 1956 dividend model Lintner 1956 dividend policy paper DOI'})
    ✅ Result (web_search): [{"title": "The Lintner model revisited: Dividends versus total payouts", "url": "https://www.scienc...
    🔧 Tool called -> web_search({'query': "meta-analysis determinants of dividend policy review 2015 2025 'dividend policy' 'meta-an...)
    ✅ Result (web_search): [{"title": "Western Energy Services Corp. Releases Third Quarter 2015", "url": "https://finance.yaho...
    🔧 Tool called -> web_search({'query': "meta-analysis determinants of dividend policy review 2010 2022 'dividend determinants' 'm...)
    ✅ Result (web_search): [{"title": "Dividend Policy and Firm Performance of Listed Consumer Goods", "url": "https://dj.univ-...
    🔧 Tool called -> web_search({'query': "review of empirical literature on dividend policy determinants 'literature review' 'divid...)
    ✅ Result (web_search): [{"title": "A bibliometric review of dividend policy literature", "url": "https://www.sciencedirect....
    🔧 Tool called -> web_search({'query': "Bhattacharya 1979 'imperfect information and dividend policy' PDF Bhattacharya 1979 divid...)
    ✅ Result (web_search): [{"title": "Imperfect information, dividend policy, and \"the bird in the ... - JSTOR", "url": "http...
    🔧 Tool called -> web_search({'query': "Miller Modigliani 1961 dividend policy 'irrelevance' paper PDF 'The Cost of Capital, Corp...)
    ...
```
