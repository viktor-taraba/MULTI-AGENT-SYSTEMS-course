from datetime import datetime
from langfuse import get_client
from dotenv import load_dotenv
load_dotenv()

# for prompts
langfuse_prompts = get_client()

LLM_POWERFUL: str = "openai:gpt-5.4"  # for planning, evaluation, supervision
LLM_FAST: str = "openai:gpt-5.4-nano" # for execution, simple tasks
LLM_test: str = "gpt-5.4-mini"
to_save_graph_image: int = 1
recursion_limit: int = 50

# Business Analyst (Planning) - planner agent
Business_Analyst_SYSTEM_prompt = langfuse_prompts.get_prompt("Business_Analyst_SYSTEM_prompt", label="production").compile()

# Developer (Execution) - coder agent
Coder_SYSTEM_prompt = langfuse_prompts.get_prompt("Coder_SYSTEM_prompt", label="production").compile()

# QA Engineer (Assurance) - reviewer agent
Reviewer_SYSTEM_prompt = langfuse_prompts.get_prompt("Reviewer_SYSTEM_prompt", label="production").compile()

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