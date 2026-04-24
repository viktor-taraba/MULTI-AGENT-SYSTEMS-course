# розбити на етап генерації та збереження результатів (в окрему папку навіть можна) та етап оцінкиз тестами (з цього json)
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
import json

with open("golden_dataset.json", "r", encoding="utf-8") as f:
    golden_data = json.load(f)

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

    test_cases = []
    tc = LLMTestCase(
        input=user_input,
        actual_output=final_answer,
        expected_output=expected_output,
    )
    test_cases.append(tc)

# !!!!!!!!!!!! зберегти

# python -m tests.test_e2e