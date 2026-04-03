from langchain.agents import create_agent

# to delete
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from schemas import CritiqueResult
from config import critic_model_name, SYSTEM_PROMPT_critic
from tools import web_search, read_url, knowledge_search, stock_company_info, find_articles_crossref

critic_agent = create_agent(
    model=critic_model_name,
    tools=[web_search, read_url, knowledge_search, stock_company_info, find_articles_crossref],
    system_prompt=SYSTEM_PROMPT_critic,
    response_format=CritiqueResult,
)