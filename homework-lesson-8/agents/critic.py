from langchain.agents import create_agent
from schemas import CritiqueResult
from config import (
    critic_model_name, 
    SYSTEM_PROMPT_critic
)
from tools import (
    web_search, 
    read_url, 
    knowledge_search, 
    stock_company_info, 
    find_articles_crossref
)
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer

custom_serializer = JsonPlusSerializer(
    allowed_msgpack_modules=[('schemas', 'CritiqueResult')]
)
memory = InMemorySaver(serde=custom_serializer)

critic_agent = create_agent(
    model=critic_model_name,
    tools=[web_search, read_url, knowledge_search, stock_company_info, find_articles_crossref],
    system_prompt=SYSTEM_PROMPT_critic,
    response_format=CritiqueResult,
    checkpointer=memory
)