# Завдання: Research Agent

Агент запускається з терміналу (python main.py) та працює в інтерактивному режимі — користувач вводить запитання, отримує відповідь, і може продовжити діалог
Агент підтримує зв'язний діалог — пам'ятає попередні повідомлення в межах сесії.

Приклад:
тут гіфка

Файл залежностей — requirements.txt

Для коректної роботи потріен [API-ключ OpenAI](https://platform.openai.com/) та створений файл .env з вказаним ключем: OPENAI_API_KEY=<тут_ваш_ключ>

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