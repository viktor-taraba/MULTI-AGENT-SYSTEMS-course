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

critic_agent = create_agent(
    model=critic_model_name,
    tools=[web_search, read_url, knowledge_search, stock_company_info, find_articles_crossref],
    system_prompt=SYSTEM_PROMPT_critic,
    response_format=CritiqueResult
)