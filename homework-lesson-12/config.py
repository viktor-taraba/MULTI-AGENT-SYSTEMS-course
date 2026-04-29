from datetime import datetime
from langfuse import get_client
from dotenv import load_dotenv
load_dotenv()

# for prompts
langfuse_prompts = get_client()

#supervisor agent
supervisor_model_name: str = "gpt-5-mini"
output_dir: str = "output"
max_iterations_supervisor: int = 100
debug_prints: int = 1
SUPERVISOR_PROMPT = langfuse_prompts.get_prompt("SUPERVISOR_PROMPT", label="production").compile()

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
max_search_results: int = 4
max_url_content_length: int = 4000
email_crossref_api: str =  "youremail@gmail.com" # optional, email for the crossref "Polite Pool"
desired_keys_yfinance: list = ['country', 'industry', 'sector', 'website', 'longBusinessSummary', 'fullTimeEmployees', 'fiveYearAvgDividendYield', 'beta', 'trailingPE',
                'forwardPE', 'marketCap', 'nonDilutedMarketCap', 'previousClose', 'fiftyTwoWeekLow', 'fiftyTwoWeekHigh', 'allTimeHigh', 'fiftyDayAverage',
                'twoHundredDayAverage', 'trailingEps', 'forwardEps', 'recommendationKey', 'numberOfAnalystOpinions', 'totalCash','totalCashPerShare','ebitda',
                'totalDebt','quickRatio','currentRatio','totalRevenue','debtToEquity','revenuePerShare','returnOnAssets','returnOnEquity','grossProfits',
                'freeCashflow','operatingCashflow','earningsGrowth','revenueGrowth','grossMargins','ebitdaMargins','operatingMargins','shortName','longName']
period_yfinance: str = "3mo"
tool_preview_len: int = 100

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