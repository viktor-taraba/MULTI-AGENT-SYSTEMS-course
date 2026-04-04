from pydantic import BaseModel, Field, max_items_critic
from typing import List, Literal

class CritiqueResult(BaseModel):
    verdict: Literal["APPROVE", "REVISE"]
    is_fresh: bool = Field(description="Is the data up-to-date and based on recent sources?")
    is_complete: bool = Field(description="Does the research fully cover the user's original request?")
    is_well_structured: bool = Field(description="Are findings logically organized and ready for a report?")
    strengths: list[str] = Field(description="What is good about the research",max_items=max_items_critic)
    gaps: list[str] = Field(description="What is missing, outdated, or poorly structured",max_items=max_items_critic)
    revision_requests: list[str] = Field(description="Specific things to fix if verdict is REVISE",max_items=max_items_critic)

class ResearchPlan(BaseModel):
    goal: str = Field(description="What we are trying to answer")
    search_queries: list[str] = Field(description="Specific queries to execute")
    sources_to_check: list[str] = Field(description="'web_search', 'read_url', 'knowledge_search', 'stock_company_info', 'find_articles_crossref' or several tools (e.g. 'web_search and read_url')")
    output_format: str = Field(description="What the final report should look like")

class ResearchResult(BaseModel):
    research_output: str = Field(description="Prepared research")