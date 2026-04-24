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
import json
import os

with open("tests/golden_dataset.json", "r", encoding="utf-8") as f:
    golden_data = json.load(f)

results_data = []
for i, data in enumerate(golden_data):
    user_input = data["input"]
    expected_output = data["expected_output"]
    category = data["category"]

    config = {
        "configurable": {"thread_id": f"supervisor_thread{i}"}, 
        "recursion_limit": max_iterations_supervisor}

    supervisor = create_agent(
                model=supervisor_model_name,
                tools=[plan, research, critique, save_report],
                system_prompt=SUPERVISOR_PROMPT,
                checkpointer=InMemorySaver(),
                )

    response = supervisor.invoke({"messages": [("user", user_input)]}, config=config)
    final_answer = response['messages'][-1].content

    print(f"Generated answer preview: {final_answer[:150]}...\n")

    results_data.append({
            "input": user_input,
            "expected_output": expected_output,
            "actual_output": final_answer,
            "category": category
        })

    # to delete
    if i >= 1:
        break

os.makedirs("tests/e2e_results", exist_ok=True)
results_path = "tests/e2e_results/generated_responses.json"

existing_data = []
if os.path.exists(results_path):
    with open(results_path, "r", encoding="utf-8") as f:
        try:
            existing_data = json.load(f)
        except:
            existing_data = []

existing_data.extend(results_data)
with open(results_path, "w", encoding="utf-8") as f:
    json.dump(existing_data, f, ensure_ascii=False, indent=4)
        
print(f"\n✅ Generation complete. Results saved to {results_path}")

# python -m tests.test_e2e_generate