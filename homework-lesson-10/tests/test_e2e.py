# тут треба ще принтів позбуватися, мабуть через додатковий параметр 0 або 1 для суб-агентів (щоб нічого не друкувалося в процесі їх роботи)
# тут по golden dataset зробити підмножину, не всі відразу
# плюс погратися з reasoning моделі
# як альтернатива - якщо продовжуватимуме використвоувати save_report, то тоді можна буде через порівняння по даті і часу виводити фінальний 
# звіт звідти, порівнюючи по даті і часу запуску та збереження звіту 

from supervisor import (
    plan,
    research,
    critique
    )
import supervisor
from config import (
    SUPERVISOR_PROMPT, 
    supervisor_model_name, 
    max_iterations_supervisor
    )
from tools import save_report
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from deepeval.dataset import EvaluationDataset
from deepeval.metrics import GEval, AnswerRelevancyMetric
from deepeval import evaluate

golden_data = [
    {
        "input": "What is pbir format (Power BI reports)? At your final step do not save the report but just print if for me as your final and only answer",
        "expected_output": "Detailed report with description of project sructure, data formats and types and at least one example of real report structure"
    },
    {
        "input": "kshdjg ksjdsjgd kj?",
        "expected_output": "Should ask for clarification or ask to write question again."
    },
]

# user_input = "What is Ponziani opening? At your final step do not save the report but just print if for me as your final and only answer"

for i, data in enumerate(golden_data):
    print()
    user_input = data["input"]
    expected_output = data["expected_output"]

    # to delete
    print(user_input)
    print(expected_output)
    print()

    config = {
        "configurable": {"thread_id": f"supervisor_thread{i}"}, 
        "recursion_limit": max_iterations_supervisor}

    # це не прописувати тут, а няпрму у файлі supervisor (через ф-ю), і далі використовувати саме її (return supervisor)
    supervisor = create_agent(
                model=supervisor_model_name,
                tools=[plan, research, critique, save_report],
                system_prompt=SUPERVISOR_PROMPT,
                checkpointer=InMemorySaver(),
                )

    response = supervisor.invoke({"messages": [("user", user_input)]}, config=config)
    final_answer = response['messages'][-1].content

    # to delete
    print(final_answer[:500])

    test_cases = []
    tc = LLMTestCase(
        input=user_input,
        actual_output=final_answer,
        expected_output=expected_output,
    )
    test_cases.append(tc)
    
    # to delete
    print(test_cases)

dataset = EvaluationDataset()
for tc in test_cases:
    dataset.add_test_case(tc)
print(f"\nGolden Dataset created: {len(dataset.test_cases)} test cases")
print("\nThis dataset can be saved and versioned for regression testing")

correctness = GEval(
    name="Correctness",
    evaluation_steps=[
        "Check whether the facts in 'actual output' contradict any facts in 'expected output'",
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

relevancy = AnswerRelevancyMetric(threshold=0.7, model="gpt-5.4-mini")

print("Running full evaluation on Golden Dataset...")
results = evaluate(
    test_cases=dataset.test_cases,
    metrics=[correctness, relevancy],
)

# python -m tests.test_e2e