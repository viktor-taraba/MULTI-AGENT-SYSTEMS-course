from langchain.agents import create_agent
from schemas import CodeOutput
from config import (
    LLM_FAST, 
    Coder_SYSTEM_prompt
)
from tools import (
    web_search, 
    knowledge_search,
    read_url,
    get_table_structure,
    execute_sql_query,
    ask_user_for_clarification,
    list_schemas_and_tables,
    get_sample_rows,
    get_view_definition
)
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer

custom_serializer = JsonPlusSerializer(
    allowed_msgpack_modules=[('schemas', 'CodeOutput')]
)
memory = InMemorySaver(serde=custom_serializer)

coder = create_agent(
    model=LLM_FAST,
    tools=[knowledge_search,web_search,read_url,get_table_structure,execute_sql_query,ask_user_for_clarification,list_schemas_and_tables,get_sample_rows,get_view_definition],
    system_prompt=Coder_SYSTEM_prompt,
    response_format=CodeOutput,
    checkpointer=memory,
    name="coder",
)