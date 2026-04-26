# Домашнє завдання: тестування мультиагентної системи (розширення hw8)

### Що змінюється порівняно з homework-8

| Було (homework-lesson-8) | Стає (homework-lesson-10)                    |
|-|----------------------------------------------|
| Мультиагентна система без тестів | Та сама система + покриття тестами           |
| Якість перевіряється вручну (vibe check) | Автоматизовані evals з метриками 0–1         |
| Немає golden dataset | 12 golden examples (happy path + edge cases + failure cases) для regression testing |
| Немає CI-ready тестів | запуск тестів через pytest |

#### Тести

|Назва тесту|Якого агента тестуємо|Що перевіряємо|
|--|--|--|
|test_plan_quality|Planner|Структуру та якість плану|
|test_plan_has_queries|Planner|Наявність пошукових запитів в search_queries та їх релевантність|
|test_query_diversity|Planner|Широта та повнота покриття питання запитами|
|||
|||
|||

Використовую pytest напряму замість deepeval

Протестуйте кожного суб-агента окремо.

**Planner Agent — структурованість плану:**

```python
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams

plan_quality = GEval(
    name="Plan Quality",
    evaluation_steps=[
        "Check that the plan contains specific search queries (not vague)",
        "Check that sources_to_check includes relevant sources for the topic",
        "Check that the output_format matches what the user asked for",
    ],
    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
    model="gpt-5.4-mini",
    threshold=0.7,
)
```

**Critic Agent — якість критики:**

```python
critique_quality = GEval(
    name="Critique Quality",
    evaluation_steps=[
        "Check that the critique identifies specific issues, not vague complaints",
        "Check that revision_requests are actionable (researcher can act on them)",
        "If verdict is APPROVE, gaps list should be empty or contain only minor items",
        "If verdict is REVISE, there must be at least one revision_request",
    ],
    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
    model="gpt-5.4-mini",
    threshold=0.7,
)
```

**Research Agent — groundedness відповіді:**

```python
groundedness = GEval(
    name="Groundedness",
    evaluation_steps=[
        "Extract every factual claim from 'actual output'",
        "For each claim, check if it can be directly supported by 'retrieval context'",
        "Claims not present in retrieval context count as ungrounded, even if true",
        "Score = number of grounded claims / total claims",
    ],
    evaluation_params=[
        LLMTestCaseParams.ACTUAL_OUTPUT,
        LLMTestCaseParams.RETRIEVAL_CONTEXT,
    ],
    model="gpt-5.4-mini",
    threshold=0.7,
)
```

#### 3. Тести Tool Correctness

Перевірте, що агенти викликають правильні інструменти:

```python
from deepeval.test_case import LLMTestCase, ToolCall
from deepeval.metrics import ToolCorrectnessMetric

# Planner should use web_search and/or knowledge_search for exploration
# Researcher should use web_search, read_url, knowledge_search
# Critic should verify facts via web_search

tool_metric = ToolCorrectnessMetric(threshold=0.5, model="gpt-5.4-mini")
```

Створіть мінімум 3 тест-кейси для tool correctness:
- Planner отримує запит → має викликати пошукові інструменти
- Researcher отримує план → має використати інструменти згідно з `sources_to_check`
- Supervisor отримує APPROVE від Critic → має викликати `save_report`

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

Запустіть evaluation на повному golden dataset і збережіть результати.

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

---

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
