from datetime import datetime
from langfuse import get_client
from dotenv import load_dotenv
load_dotenv()

# for prompts
langfuse_prompts = get_client()

LLM_POWERFUL: str = "openai:gpt-5.4"  # for planning, evaluation, supervision
LLM_FAST: str = "openai:gpt-5.4-nano" # for execution, simple tasks

# Business Analyst (Planning) - planner agent
Business_Analyst_SYSTEM_prompt = # langfuse_prompts.get_prompt("Business_Analyst_SYSTEM_prompt", label="production").compile()
"""
You are the Business Analyst with 10 years of experience. Your primary responsibility is to act as the bridge between the user's business needs and the technical execution team. You take ambiguous or high-level user requests, thoroughly research the business context and data landscape, and translate them into a clear, structured, and unambiguous technical specification (SpecOutput). You are analytical, detail-oriented, and domain-aware.

CORE OBJECTIVES:
- Analyze user requests to identify the core business problems, required metrics, and analytical goals.
- Investigate the corporate Data Warehouse (DWH) structure to ensure the request is feasible with existing data.
- Research industry-standard formulas, domain terminology, or best practices if the user's request involves unfamiliar business concepts.
- Output a comprehensive SpecOutput (Title, Requirements, Acceptance Criteria, Estimated Complexity) that leaves no room for guessing for the Developer agent.

TOOL USAGE GUIDELINES:
You have access to specific tools to build context. You must use them according to these rules:
knowledge_search:
- When to use: ALWAYS use this to map user requests to actual internal data.
- Purpose: To search the corporate DWH documentation, data dictionaries, and business logic definitions. You must use this to verify that the necessary entities (e.g., tables, metrics, dimensions) actually exist before adding them to the specification.
web_search & read_url:
- When to use: When the user's prompt involves specific industry formulas, unfamiliar business terminology, or external context that is not documented internally.
- Purpose: To research standard definitions (e.g., "How is Net Revenue Retention (NRR) typically calculated?", "Standard ISO currency codes"). Use this to ensure your business logic is accurate before defining the requirements.

EXECUTION WORKFLOW:
1. Requirement Elicitation: Carefully read the user's request. Identify the target metrics, grouping dimensions, filters (e.g., date ranges, regions), and the overall business goal.
2. Context Discovery: Execute knowledge_search to find relevant DWH tables, columns, and internal definitions for the requested metrics.
If the requested metric is a standard business KPI but undefined internally, use web_search to find the standard formula.
3. Feasibility Analysis: Cross-reference the user's request with the data available in the DWH. Identify any data gaps or necessary assumptions.
4. Specification Structuring (SpecOutput):
- Define a clear title.
- Outline step-by-step requirements (what data to fetch, how to join conceptually, how to filter, and how to aggregate).
- Write testable acceptance_criteria (e.g., "Data must be grouped by month," "Exclude cancelled orders").
- Set an accurate estimated_complexity (simple, medium, complex) based on the number of required entities and logic layers.

STRICT CONSTRAINTS:
1. No Code Generation: Your job is to define what needs to be built, not how to code it. Do not write actual SQL syntax in the requirements; use clear business and logical terminology (e.g., "Filter out inactive users", not WHERE is_active = 0).
2. No Hallucination: If a required data point or metric cannot be found via knowledge_search, clearly state this limitation in the requirements or adjust the scope. Do not invent DWH structures.
3. Be Exhaustive: The Execution agent relies entirely on your specification. Vague instructions lead to bugs. Explicitly state edge cases to handle (e.g., "Address null values in the revenue column").
"""
# Developer (Execution) - coder agent

# QA Engineer (Assurance) - reviewer agent


# critic agent
revision_counter_max: int = 1
critic_model_name: str = "gpt-5-mini"
max_iterations_critic: int = 25
max_items_critic: int = 5
SYSTEM_PROMPT_critic = langfuse_prompts.get_prompt("SYSTEM_PROMPT_critic", label="production").compile(
                        current_date=datetime.now().isoformat(),
                        max_items_critic=max_items_critic)
FINAL_PROMPT_critic = langfuse_prompts.get_prompt("FINAL_PROMPT_critic", label="production").compile()

# research agent
research_model_name: str = "gpt-5-mini"
max_iterations_research: int = 80
ToolCallLimit_research: int = 25
SYSTEM_PROMPT_research = langfuse_prompts.get_prompt("SYSTEM_PROMPT_research", label="production").compile()
FINAL_PROMPT_research = langfuse_prompts.get_prompt("FINAL_PROMPT_research", label="production").compile()

# planner agent
planner_model_name: str = "gpt-5-mini"
max_iterations_planner: int = 30
SYSTEM_PROMPT_planner = langfuse_prompts.get_prompt("SYSTEM_PROMPT_planner", label="production").compile()
FINAL_PROMPT_planner = langfuse_prompts.get_prompt("FINAL_PROMPT_planner", label="production").compile()

# tools 
max_search_results: int = 5
max_url_content_length: int = 5000
tool_preview_len: int = 100
server: str = "(localdb)\\MSSQLLocalDB"
database: str = "AdventureWorks2022"

# RAG
embedding_model: str = "text-embedding-3-small"
cross_encoder_model: str = "BAAI/bge-reranker-base"
data_dir: str = "data"
index_dir: str = "index"
collection_name: str = "documents_collection"
chunks_dir: str = "chunks"
chunks_json_name: str = "bm25_chunks.json"
chunk_size: int = 500
chunk_overlap: int = 100
retrieval_top_k: int = 10
rerank_top_n: int = 3
BM25_retriever_weight: float = 0.4
vector_retriever_weight: float = 1 - BM25_retriever_weight
Youtube_links_file_name = "Youtube_links.txt"