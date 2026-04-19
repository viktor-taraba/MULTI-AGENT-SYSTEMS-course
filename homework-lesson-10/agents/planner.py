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
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer

custom_serializer = JsonPlusSerializer(
    allowed_msgpack_modules=[('schemas', 'ResearchPlan')]
)
memory = InMemorySaver(serde=custom_serializer)

planner_agent = create_agent(
    model=planner_model_name,
    tools=[web_search, knowledge_search],
    system_prompt=SYSTEM_PROMPT_planner,
    response_format=ResearchPlan,
    checkpointer=memory
)