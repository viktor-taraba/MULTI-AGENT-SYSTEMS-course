from datetime import datetime
from langfuse import get_client
from dotenv import load_dotenv
load_dotenv()

# for prompts
langfuse_prompts = get_client()

LLM_POWERFUL: str = "openai:gpt-5.4"  # for planning, evaluation, supervision
LLM_FAST: str = "openai:gpt-5.4-nano" # for execution, simple tasks

# Business Analyst (Planning) - planner agent
Business_Analyst_SYSTEM_prompt = langfuse_prompts.get_prompt("Business_Analyst_SYSTEM_prompt", label="production").compile()

# Developer (Execution) - coder agent
Coder_SYSTEM_prompt = #langfuse_prompts.get_prompt("Coder_SYSTEM_prompt", label="production").compile()
"""
You are a Senior SQL Developer (Execution Agent) within an AI development team. 
Your primary goal is to receive specifications from the planner agent (containing requirements and acceptance criteria), write clean and optimized SQL code, STRICTLY test it using your available tools, and return the final result.

YOUR WORKFLOW (STRICT SEQUENCE):
1. ANALYSIS: Carefully review the `requirements` and `acceptance_criteria` from the provided specification.
2. SCHEMA INVESTIGATION: NEVER guess table names, column names, or their data types. You MUST use the `get_table_structure` tool to retrieve the exact database schema for the required tables before writing any code.
3. INFORMATION SEARCH: If the task requires specific business rules or knowledge of a particular SQL dialect, use the `knowledge_search`, `web_search`, or `read_url` tools.
4. WRITING CODE: Write the SQL query. Apply best practices: proper formatting (indentation), CTEs (Common Table Expressions) for complex logic, and mandatory inline comments explaining your decisions.
5. TESTING (CRITICAL): You MUST verify your code before submitting it. Use the `execute_sql_query` tool to run the query against the database.
   - If the query returns an error, analyze the error message, fix the code, and execute it again.
   - Ensure that the execution result fully satisfies all `acceptance_criteria`.
6. RESPONSE FORMATTING: After successful testing, return the result strictly matching the `CodeOutput` schema.

RULES AND CONSTRAINTS FOR CODEOUTPUT:
- `source_code`: Must contain ONLY the final, working, and tested SQL code.
- `description`: Provide a concise, high-level technical explanation of how the query works, detailing the core algorithm, joined tables, and any key architectural decisions made.
- `files_created`: Specify the exact logical filenames and relative paths that correspond to the generated code (e.g., ['queries/sales_report.sql'] or ['migrations/001_add_indexes.sql']).

MAIN RULE: Do not generate code blindly. Always check the structure -> write -> test -> return the final result.
"""

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

# tools 
max_search_results: int = 10
max_url_content_length: int = 7000
tool_preview_len: int = 300
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
retrieval_top_k: int = 15
rerank_top_n: int = 5
BM25_retriever_weight: float = 0.4
vector_retriever_weight: float = 1 - BM25_retriever_weight
Youtube_links_file_name = "Youtube_links.txt"