from langchain.agents import create_agent

# to delete
#import os, sys
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from schemas import ResearchPlan
from config import (
    planner_model_name, 
    SYSTEM_PROMPT_planner
)
from tools import (
    web_search, 
    knowledge_search
)

planner_agent = create_agent(
    model=planner_model_name,
    tools=[web_search, knowledge_search],
    system_prompt=SYSTEM_PROMPT_planner,
    response_format=ResearchPlan,
)

"""
# Test Planner Agent in isolation
for step in planner_agent.stream({
    "messages": [
        {
            "role": "user",
            "content": "pbir files validation"
        }
    ]
}):
    for update in step.values():
        for message in update.get("messages", []):
            message.pretty_print()


result = planner_agent.invoke({
    "messages": [{"role": "user", "content": "pbir files validation"}]
})

plan = result["structured_response"]
print(plan.model_dump_json(indent=4))
"""