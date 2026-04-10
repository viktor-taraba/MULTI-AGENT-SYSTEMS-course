from langchain.agents import create_agent
from config import (
    research_model_name, 
    SYSTEM_PROMPT_research,
    ToolCallLimit_research
)
from schemas import ResearchResult
from tools import (
    web_search, 
    read_url, 
    knowledge_search, 
    stock_company_info, 
    find_articles_crossref
)
from langchain.agents.middleware.tool_call_limit import ToolCallLimitMiddleware

tool_limiter = ToolCallLimitMiddleware(
    run_limit=ToolCallLimit_research, 
    exit_behavior="error"
)

research_agent = create_agent(
    model=research_model_name,
    tools=[web_search, read_url, knowledge_search, stock_company_info, find_articles_crossref],
    system_prompt=SYSTEM_PROMPT_research,
    response_format=ResearchResult,
    middleware=[tool_limiter]
)