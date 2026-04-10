from langchain.agents import create_agent
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
    response_format=ResearchPlan
)