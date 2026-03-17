# Завдання: Research Agent

Агент запускається з терміналу (python3 main.py) та працює в інтерактивному режимі — користувач вводить запитання, отримує відповідь, і може продовжити діалог.
Агент підтримує зв'язний діалог — пам'ятає попередні повідомлення в межах сесії.

Для коректної роботи потрібен [API-ключ OpenAI](https://platform.openai.com/) та створений файл .env з вказаним ключем: `OPENAI_API_KEY=<тут_ваш_ключ>`

Файл залежностей — requirements.txt

### Приклад:

![Demo](/homework-lesson-3/gif%20example/agent_example.gif)

Приклади згенерованих звітів - в [output](/homework-lesson-3/output)

### Опис тулів для агента:
|Назва|Параметри|Опис|
|--|--|--|
|`web_search`|`query: str`|Шукає актуальну інформацію в інтернеті через DuckDuckGo. Повертає перелік знайдених посилань з даними про заголовок, URL, фрагмент тексту. Використовується як перший крок пошуку.|
|`read_url`|`url: str`|Отримує основний текст із вебсторінки (або PDF, якщо це пряме посилання на pdf-звіт чи статтю).|
|`stock_company_info`|`stock_ticker: str, result_type: str`|Отримує фінансові дані або загальний профіль компанії через Yahoo Finance API.|
|`find_articles_crossref`|`query: str`|Шукає наукові статті в базі Crossref. Повертає відфільтрований список записів із валідною анотацією (назва, анотація, DOI, рік).|
|`write_report`|`filename: str, content: str`|Зберігає фінальний звіт у форматі Markdown, використовується як останній крок для видачі результату.|

### Структура проєкту

```
homework-lesson-3/
├── main.py              # Entry point
├── agent.py             # Agent setup (LLM, tools, memory, create_agent)
├── tools.py             # Tool definitions and implementations
├── config.py            # System prompt, settings, constants
├── requirements.txt     # Libraries list + min version for each library
├── output/
│   └── MSFT_vs_NVDA_investment_comparison.md                   # Example generated report (#1)
│   └── payment_system_risks_review.md                          # Example generated report (#2)
│   └── RAG_comparison_naive_sentence-window_parent-child.md    # Example generated report (#3)
│   └── dividend_policy_report.md                               # Example generated report (#4)
└── README.md            # Setup instructions, architecture overview
```
