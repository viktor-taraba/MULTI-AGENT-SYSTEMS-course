from langchain.agents import create_agent
from schemas import SpecOutput
from config import (
    LLM_POWERFUL, 
    Business_Analyst_SYSTEM_prompt
)
from tools import (
    web_search, 
    knowledge_search,
    read_url,
    ask_user_for_clarification,
    list_schemas_and_tables,
    get_sample_rows,
    get_view_definition
)
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer

custom_serializer = JsonPlusSerializer(
    allowed_msgpack_modules=[('schemas', 'SpecOutput')]
)
memory = InMemorySaver(serde=custom_serializer)

planner = create_agent(
    model=LLM_POWERFUL,
    tools=[knowledge_search,web_search,read_url,ask_user_for_clarification,list_schemas_and_tables,get_sample_rows,get_view_definition],
    system_prompt=Business_Analyst_SYSTEM_prompt,
    response_format=SpecOutput,
    checkpointer=memory,
    name="planner",
)