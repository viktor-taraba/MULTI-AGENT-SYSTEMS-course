from langchain.agents import create_agent

# to delete
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import research_model_name, SYSTEM_PROMPT_research, max_iterations_research
from schemas import ResearchResult
from tools import web_search, read_url, knowledge_search, stock_company_info, find_articles_crossref

research_agent = create_agent(
    model=research_model_name,
    tools=[web_search, read_url, knowledge_search, stock_company_info, find_articles_crossref],
    system_prompt=SYSTEM_PROMPT_research,
    response_format=ResearchResult
)

"""
#config = {"recursion_limit": max_iterations_research, "early_stopping_method": "generate"}

# Test Planner Agent in isolation
for step in research_agent.stream({
    "messages": [
        {
            "role": "user",
            "content": "pbir files validation"
        }
    ]
}):#, config = config):
    for update in step.values():
        for message in update.get("messages", []):
            message.pretty_print()
"""