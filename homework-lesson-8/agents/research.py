from langchain.agents import create_agent

from config import (
    research_model_name, 
    SYSTEM_PROMPT_research
)
from schemas import ResearchResult
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
    allowed_msgpack_modules=[('schemas', 'ResearchResult')]
)
memory = InMemorySaver(serde=custom_serializer)

research_agent = create_agent(
    model=research_model_name,
    tools=[web_search, read_url, knowledge_search, stock_company_info, find_articles_crossref],
    system_prompt=SYSTEM_PROMPT_research,
    response_format=ResearchResult,
    checkpointer=memory
)