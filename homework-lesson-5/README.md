# Завдання: Research Agent з RAG-системою

### Що змінюється порівняно з попередніми homework

| Було (homework-lesson-3)                        | Стає (homework-lesson-5) |
|-------------------------------------------------|---|
| Tools: `web_search`, `read_url`, `write_report` | + новий tool: `knowledge_search` |
| Агент шукає лише в інтернеті                    | Агент шукає і в інтернеті, і в локальній базі знань |
|                                                 | Є pipeline для завантаження документів у векторну БД |
|                                                 | Hybrid search (semantic + BM25) з cross-encoder reranking |

---

### Що потрібно реалізувати

#### 1. Knowledge Ingestion Pipeline (`ingest.py`)

Скрипт, який завантажує документи у векторну базу даних:

- **Завантаження документів** — PDF файли з директорії `./data/`
- **Chunking** — розбиття на чанки з `RecursiveCharacterTextSplitter` (або semantic chunking — за бажанням)
- **Embeddings** — використайте `text-embedding-3-small` або `text-embedding-3-large`
- **Векторна БД** — оберіть одну з: FAISS (для простоти), Qdrant, Chroma, або pgvector
- **Збереження індексу** — індекс повинен зберігатися на диск і перезавантажуватися без повторного embedding

Скрипт запускається окремо: `python ingest.py` — і створює/оновлює індекс.

#### 2. Hybrid Retrieval з Reranking (`retriever.py`)

Модуль, що реалізує пошук по базі знань:

- **Semantic search** — пошук за cosine similarity у векторній БД
- **BM25 search** — лексичний пошук за ключовими словами
- **Ensemble** — об'єднання результатів semantic + BM25 (наприклад, через `EnsembleRetriever` або вручну)
- **Reranking** — cross-encoder reranker (наприклад, `BAAI/bge-reranker-base`) для фільтрації шуму

#### 3. RAG Tool для агента (`tools.py`)

Новий tool `knowledge_search`, який агент використовує поряд з `web_search`, `read_url`, `write_report`:

```python
def knowledge_search(query: str) -> str:
    """Search the local knowledge base. Use for questions about ingested documents."""
    ...
```

Агент сам вирішує, коли шукати в інтернеті (`web_search`), а коли — в локальній базі (`knowledge_search`).

#### 4. Тестові дані (`data/`)

У `./data/` вже є декілька документів для тестування. За бажанням, додайте ще для перевірки роботи системи з різними типами.

---

### Структура проекту

```
homework-lesson-5/
├── main.py              # Entry point (з homework-lesson-3/4, адаптований)
├── agent.py             # Agent setup з новим knowledge_search tool
├── tools.py             # web_search, read_url, write_report, knowledge_search
├── retriever.py         # Hybrid retrieval + reranking logic
├── ingest.py            # Ingestion pipeline: docs → chunks → embeddings → vector DB
├── config.py            # Settings
├── requirements.txt     # Залежності
├── data/                # Документи для ingestion
│   └── (ваші PDF/TXT файли)
└── .env                 # API ключі (не комітити!)
```

---

### Очікуваний результат

1. **Ingestion працює** — `python ingest.py` завантажує документи з `./data/` та створює індекс
2. **Hybrid search** — пошук використовує і semantic, і BM25, результати об'єднуються
3. **Reranking** — cross-encoder фільтрує нерелевантні результати
4. **Агент використовує RAG** — агент самостійно вирішує, коли шукати в базі знань, а коли в інтернеті
5. **Multi-step reasoning** — агент комбінує результати з різних джерел (web + knowledge base)
6. **Звіт** — агент генерує Markdown-звіт з посиланнями на джерела

Приклад логу в консолі:
```
Research Agent
type 'exit' or 'quit' to quit
'delete history' to delete full conversation history (including previous conversations) and exit
----------------------------------------------------------------------------------------------------

You: Що таке RAG і які є підходи до retrieval?

🔄 Iteration 1 - Thinking...
🔧 Tool called -> knowledge_search({'query': 'RAG retrieval augmentation generation approaches retrieval types'})
Loading weights: 100%|██████████| 201/201 [00:00<00:00, 8243.34it/s]
✅ Result (knowledge_search): --- Document 1 ---
Source: retrieval-augmented-generation.pdf (Page: 0)
Content:
Retrieval-augmented...

🔄 Iteration 2 - Thinking...
🔧 Tool called -> web_search({'query': 'Retrieval-augmented generation RAG approaches to retrieval vector dense sparse BM25 hybri...)
✅ Result (web_search): [{"title": "Retrieval-augmented generation - Wikipedia", "url": "https://en.wikipedia.org/wiki/Retri...

🔄 Iteration 3 - Thinking...
🔧 Tool called -> read_url({'url': 'https://en.wikipedia.org/wiki/Retrieval-augmented_generation'})
✅ Result (read_url): Retrieval-augmented generation
Retrieval-augmented generation (RAG) is a technique that enables larg...

🔄 Iteration 4 - Thinking...
🔧 Tool called -> read_url({'url': 'https://medium.com/@yashwanths_29644/retrieval-augmented-generation-rag-06-bm25-retriever-w...)
✅ Result (read_url): Error: Unable to fetch content from 'https://medium.com/@yashwanths_29644/retrieval-augmented-genera...

🔄 Iteration 5 - Thinking...
🔧 Tool called -> read_url({'url': 'https://watercrawl.dev/blog/Building-on-RAG'})
✅ Result (read_url): 🎬 Episode 2 : 🔍 Building on RAG: Exploring BM25 and Semantic Search
Ai engineer
Retrieval-Augmented ...

🔄 Iteration 6 - Thinking...
🔧 Tool called -> write_report({'filename': 'RAG_and_retrieval_approaches.md', 'content': '# RAG (Retrieval‑Augmented Generation) —...)
✅ Result (write_report): Success: Report successfully saved to C:\Users\Viktor\source\repos\MULTI-AGENT-SYSTEMS-course\homewo...

🔄 Iteration 7 - Thinking...

🤖 Agent:
Звіт успішно збережено як RAG_and_retrieval_approaches.md. Коротко: RAG — це поєднання LLM і механізму витягування зовнішніх документів для підвищення актуальності й точності відповідей; основні підходи до retrieval — sparse (BM25), dense (embedding‑based), hybrid (sparse+dense), а також neural retrievers із поділом на bi‑encoder і cross‑encoder та reranking. Документ містить рекомендації, архітектурний приклад, метрики оцінки й посилання на джерела.
```