# Порівняльний звіт: три підходи до побудови RAG — Naive, Sentence-Window та Parent-Child Retrieval

## Короткий виклад
Цей звіт порівнює три широко використовувані стратегії побудови Retrieval-Augmented Generation (RAG): "naive" (базовий), "sentence-window" (віконний на рівні речень) та "parent-child" (шукати малими шматками — повертати більші батьківські документи). Для кожного підходу наведено опис, робочий процес, переваги й недоліки, витрати (токени/latency), практичні поради впровадження, метрики оцінки та рекомендації у виборі підходу за сценарієм.

---

## 1. Визначення та короткий робочий процес

1) Naive RAG (базовий)
- Опис: індексуються/вбудовуються великі або фіксовані чанки (напр., 500–2000 токенів). Пошук виконується по цих чанках і знайдені шматки подаються без додаткового розширення в LLM.
- Робочий потік: split -> embed -> vector search(k) -> concatenate top-k chunks -> LLM prompt

2) Sentence-Window Retrieval
- Опис: розбивка на речення; кожне речення зберігається разом з його локальним контекстом (вікно сусідніх речень). При пошуку повертаються найбільш релевантні sentence-windows; це зберігає локальну звязність і підвищує точність.
- Робочий потік: sentence-split -> create windows (size w) -> embed windows -> vector search(k) -> optionally post-process metadata -> LLM prompt

3) Parent-Child Retrieval (Parent Document Retrieval / search-small-return-large)
- Опис: документи діляться на маленькі child-чанки для індексації (висока точність пошуку). Після пошуку по child'ам система знаходить відповідні parent-документи (або повертає розширений вміст батька/грань контексту) — дає повний контекст без втрати точності.
- Робочий потік: split into children + store parent -> embed children -> vector search on children(k) -> collect parent IDs -> retrieve parent document(s) or expanded windows -> LLM prompt

---

## 2. Детальне порівняння факторів

Критерії порівняння: релевантність (precision), покриття/контекст (recall/contextual completeness), шум/торення непридатної інформації, токен-кост (вартість заповнення контексту), затримка (latency), складність інженерії.

- Granularity (гранулярність)
  - Naive: низька/середня — великі чанки. Зручна, але може «змішувати» різні теми.
  - Sentence-window: висока — фокус на реченнях + локальний контекст.
  - Parent-child: дуже висока для пошуку (child), але повертає середній/великий контекст (parent).

- Context preservation (збереження контексту)
  - Naive: часто зберігає контекст, але разом з великою кількістю шуму; якщо chunk точно містить потрібний шматок — добре.
  - Sentence-window: зберігає локальну звязність без надмірного шуму.
  - Parent-child: забезпечує повний контекст батьківського документа, корисно коли відповідь потребує ширшого контексту (нормативні документи, статті).

- Precision vs. Noise
  - Naive: може повернути релевантний шматок, але часто разом із нерелевантним текстом => зниження точності відповіді LLM.
  - Sentence-window: краща точність і підвищена «groundedness» (джерельність) — менше зайвих фактів.
  - Parent-child: точний пошук child, потім повний parent => хороша баланс precision + context, але ризик додати зайвий контент родичів.

- Token cost / LLM prompt size
  - Naive: середній — залежить від розміру chunk'ів і кількості top-k. При великих чанках швидко росте вартість.
  - Sentence-window: часто найменший token-cost, бо повертаються компактні, релевантні вікна (ефективніше для generation cost).
  - Parent-child: більший token-cost якщо повертаються повні parent-документи (trade-off: компактні child для пошуку + дорогий parent для генерації).

- Latency та складність системи
  - Naive: найпростіш в реалізації; найнижча інженерна складність; низька затримка на retrieval етапі.
  - Sentence-window: невелике ускладнення (парсинг на речення, windows, metadata) — помірна latency.
  - Parent-child: вища система-сложність (збереження parent store, mapping child->parent, додаткові запити на остаточний fetch) => вища latency та складність впровадження.

- Коли краще підходить
  - Naive: прості бот-інтерфейси, невеликі документи, швидке прототипування.
  - Sentence-window: FAQ, технічна документація, коли потрібна точність на реченні/фрагменті; краща для відповідей, що вимагають «grounded» цитування.
  - Parent-child: великі документи зі структурою (статті, глави, юридичні тексти), коли потрібно знайти точний passage, але передати LLM повний контекст батька.

---

## 3. Конкретні переваги та недоліки (скорочено)

1) Naive
- Переваги: найпростіший інструмент; простота індексації; низька інженерна вартість.
- Недоліки: втрата точності, змішування тем; або надмірний токен-кост при великих чанках.

2) Sentence-window
- Переваги: краще зберігає локальний контекст, підвищує релевантність і groundedness; економніший по токенам.
- Недоліки: потребує якісного sentence-splitting (мовні особливості), може упускати «дальший» контекст, якщо вікно занадто вузьке.

3) Parent-child
- Переваги: пошук на дрібному рівні + повний контекст для генерації; добре працює з ієрархічною структурою.
- Недоліки: складніший інфраструктурно; може підвищувати токен-кост і latency при витягу parent; потрібно контролювати дублювання/повторний вміст.

---

## 4. Практичні реалізації / псевдокод / приклади

1) Naive (псевдокод)
- chunk_size = 1000 tokens
- for doc: split_by_size -> embed -> vector_db.upsert
- query: vector_db.search(query, k=5) -> concatenate -> prompt -> LLM

2) Sentence-window
- sentence_split(document)
- for each sentence i: window = sentences[i-window_size .. i+window_size]
- create node with text=window_text + metadata(original_sentence=index)
- embed nodes -> index
- query -> return top-k windows (optionally use metadata replacement) -> LLM

3) Parent-child
- parent_split_size = large (e.g., 2000 tokens) — store parents in docstore
- child_split_size = small (e.g., 200 tokens) — index children with parent_id in payload
- query -> vector_db.search(children, k=top_k) -> collect unique parent_ids -> fetch parents from docstore -> optionally window-around-matched-child inside parent -> LLM

---

## 5. Налаштування та практичні поради

- Вибір розміру chunk / window
  - Sentence-window: типово window_size = 13 (1 речення з лівого/правого або 1–2 речення по боках). Експериментуйте з 1..3.
  - Parent-child: child_size 15000 токенів; parent_size 1500000 токенів.

- Постобробка результатів пошуку
  - Для sentence-window: metadata replacement, dedupe, rerank (cross-encoder) перед передачею в LLM.
  - Для parent-child: після отримання parent можна вирізати вікно навколо matched child (windowed expansion) замість передачі цілого parent.

- Ререйтинґ/реранкінґ
  - У серйозних системах: векторний пошук (bi-encoder) + cross-encoder reranker (реранкінг) для top-N, щоб зменшити шум до LLM.

- Зниження токен-косту
  - Виконуйте агрегацію/сжаття (contextual compression) перед відправкою в LLM: LLM або heuristics виокремлюють релевантні речення.

---

## 6. Метрики та способи оцінки

- Precision@k / Recall@k
- Groundedness / Hallucination rate (ручна або semi-automatic перевірка відповідей)
- Token cost per query
- Latency (retrieval + assembly + LLM inference)
- Human evaluation (fluency, correctness, source attribution)

Емпіричні спостереження з літератури/публікацій:
- Sentence-window часто показує зростання релевантності й зниження hallucinatory facts порівняно з naive та може зменшувати загальну кількість токенів, які потребує LLM.
- Parent-child дає найкращий баланс precision+context для довгих документів, але дорожчий у токенах і затримках.

---

## 7. Рекомендації за сценаріями

- Швидкий прототип, невеликі документи, обмежений engineering budget: Naive RAG.
- FAQ, технічна документація, де окрема пропозиція/речення має значення (та потрібно мінімізувати hallucinations): Sentence-window.
- Величезні/ієрархічні документи (книги, юридичні справи, технічні специфікації), де потрібно і точне місце знаходження та розгорнутий контекст: Parent-child retrieval (search-small-return-large) + optional windowing.

---

## 8. Типові помилки та пастки

- Naive: використовувати занадто великі фіксовані чанки — призводить до шуму.
- Sentence-window: поганий sentence-splitting (особливо для мов з нестандартними роздільниками) може зіпсувати retrieval.
- Parent-child: без dedupe parent'ів і без віконної компресії — LLM отримає надмірну кількість повторів або дуже довгі документи.

---

## 9. Короткі практичні рецепти

- Почніть з sentence-window для документації/FAQ — зазвичай дає найкращий ROI (точність/вартість).
- Для великих документів використовуйте parent-child: індексуйте child однакової, невеликої довжини; пошукуйте по child; отримуйте parent і витягуйте вікно навколо збігу.
- Додайте reranker (cross-encoder) на топ-10 результатів перед формуванням prompt для LLM.
- Обовязково вимірюйте token-cost і latency в production-режимі; оптимізуйте window_size і top-k відповідно до SLA і бюджету.

---

## Висновок
- Naive RAG — швидкий і простий старт, але часто поступається у точності й гуртуванні інформації.
- Sentence-window — найкращий компроміс для завдань, де місце/речення мають значення; знижує hallucination та токен-витрати.
- Parent-child — найкращий варіант для великих структурованих корпусів, коли потрібен і точний пошук, і повний контекст; дорожчий у впровадженні й токенах.


---

## Джерела
- From Naïve Retrieval to Sentence Window Retrieval in RAG Systems — https://dev.to/diviks_1fd539c1fb4beb685b/from-naive-retrieval-to-sentence-window-retrieval-in-rag-systems-2o1c
- Parent Document Retrieval: Context Without Noise — https://app.ailog.fr/en/blog/guides/parent-document-retrieval
- Parent document retrieval with MongoDB and LangChain — https://www.mongodb.com/docs/atlas/ai-integrations/langchain/parent-document-retrieval/
- Additional background & comparisons (search results referenced):
  - https://glaforge.dev/posts/2025/02/25/advanced-rag-sentence-window-retrieval/
  - https://www.graysonadkins.com/html/notebooks/rag/sentence-window-retrieval.html
  - GitHub example (parent-child): https://github.com/kishore2797/parent-document-retrieval

