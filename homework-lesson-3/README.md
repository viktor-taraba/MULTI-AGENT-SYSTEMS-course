# Завдання: Research Agent

Агент запускається з терміналу (python3 main.py) та працює в інтерактивному режимі — користувач вводить запитання, отримує відповідь, і може продовжити діалог.
Агент підтримує зв'язний діалог — пам'ятає попередні повідомлення в межах сесії.

Для коректної роботи потрібен [API-ключ OpenAI](https://platform.openai.com/) та створений файл .env з вказаним ключем: `OPENAI_API_KEY=<тут_ваш_ключ>`

Файл залежностей — requirements.txt

### Приклад:

![Demo](/homework-lesson-3/gif%20example/agent_example.gif)

Приклади згенерованих звітів - в ![output](/homework-lesson-3/output)

### Опис тулів для агента:
|Назва|Параметри|Опис|
|--|--|--|
|web_search|query: str|Шукає актуальну інформацію в інтернеті через DuckDuckGo. Повертає перелік знайдених посилань з даними про заголовок, URL, фрагмент тексту. Використовується як перший крок пошуку.|


### Структура проєкту

```
research-agent/
├── main.py              # Entry point
├── agent.py             # Agent setup (LLM, tools, memory, create_agent)
├── tools.py             # Tool definitions and implementations
├── config.py            # System prompt, settings, constants
├── requirements.txt
├── example_output/
│   └── report.md        # Example generated report
└── README.md            # Setup instructions, architecture overview
```
