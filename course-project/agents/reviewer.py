from langchain.agents import create_agent
from schemas import ReviewOutput
from config import (
    LLM_POWERFUL, 
    Reviewer_SYSTEM_prompt
)
from tools import (
    knowledge_search,
    get_table_structure,
    execute_sql_query,
    get_sample_rows,
    get_sql_execution_plan
)
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer

custom_serializer = JsonPlusSerializer(
    allowed_msgpack_modules=[('schemas', 'ReviewOutput')]
)
memory = InMemorySaver(serde=custom_serializer)

reviewer = create_agent(
    model=LLM_POWERFUL,
    tools=[knowledge_search,get_table_structure,execute_sql_query,get_sample_rows,get_sql_execution_plan],
    system_prompt=Reviewer_SYSTEM_prompt,
    response_format=ReviewOutput,
    checkpointer=memory,
    name="reviewer",
)