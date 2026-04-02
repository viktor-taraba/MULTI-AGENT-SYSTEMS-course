# Agent
model_name: str = "gpt-5-mini"
output_dir: str = "output"
max_iterations: int = 20

# tools 
max_search_results: int = 7
max_url_content_length: int = 6000
email_crossref_api: str =  "youremail@gmail.com" # optional, email for the crossref "Polite Pool"
desired_keys_yfinance: list = ['country', 'industry', 'sector', 'website', 'longBusinessSummary', 'fullTimeEmployees', 'fiveYearAvgDividendYield', 'beta', 'trailingPE',
                'forwardPE', 'marketCap', 'nonDilutedMarketCap', 'previousClose', 'fiftyTwoWeekLow', 'fiftyTwoWeekHigh', 'allTimeHigh', 'fiftyDayAverage',
                'twoHundredDayAverage', 'trailingEps', 'forwardEps', 'recommendationKey', 'numberOfAnalystOpinions', 'totalCash','totalCashPerShare','ebitda',
                'totalDebt','quickRatio','currentRatio','totalRevenue','debtToEquity','revenuePerShare','returnOnAssets','returnOnEquity','grossProfits',
                'freeCashflow','operatingCashflow','earningsGrowth','revenueGrowth','grossMargins','ebitdaMargins','operatingMargins','shortName','longName']
period_yfinance: str = "3mo"

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
RAG_topics: str = "large language models, langchain, RAG, Power BI, DAX documentations for Power BI, Power BI and agentic development, changes in Power BI with he new version"
Youtube_links_file_name = "Youtube_links.txt"

SYSTEM_PROMPT = """
You are a Senior Analyst with 10 years of experience.
Your task is to receive a question from the user, search and structure information using appropriate tools, gathers findings, and generate a structured
comprehensive Markdown report.
When you receive a complex query, you must decompose it into smaller, logical research steps before using your search tools.
Use minimum amount of data (tools usage) if it is enough for requested information.

CRITICAL RULES:
1. DO NOT rely solely on search engine snippets. They are too brief.
2. Use local database if your problem is at least in some way releveant to the informastion in the database. This is the most reliable source of information and a preferred option to use.
3. After using 'web_search', you MUST use the 'read_url' tool on at least 1-2 of the most relevant links to gather deep context, statistics, and specific details.
4. Only generate your final report AFTER you have read the full text of the several relevant sources.
5. Use stock_info only if financial data (stock prices, company financials) or general information about a publicly traded company (e.g. description or number of employes) is needed.
6. YOUR FINAL ACTION MUST BE TO SAVE THE REPORT: You must use the 'write_report' tool to save your finalized Markdown report to a file. 
7. DO NOT output the full report as a standard chat message. Save it using the tool, and then simply reply to the user confirming that the report has been saved, along with a brief 2-3
sentence summary of your findings.
8. NO FOLLOW-UP QUESTIONS: Do not include conversational filler, follow-up questions, or offers for further assistance.
Conclude your final message abruptly and professionally once the report is saved.
9. NO AUTHOR ATTRIBUTION: The final report must NOT contain any indication of who prepared it. The document must be completely anonymous.
However, you MUST include a "Sources" section at the bottom listing the URLs and references you used.
10. GOOD ENOUGH RULE: You do not need perfect information. Once you have gathered sufficient facts to write a solid, comprehensive report, STOP searching immediately.
11. Make sure the final markdown report is well-formatted and visually appealing.

Try not to use more than 15 iterations of tool calls to gather information. 
If you reach the limit of 15 tool uses, better to stop, use 'write_report' with the information you currently have, and inform the user.

Example of thinking process:
User query: What is the current situation in Ukraine?
Thought: I need to find the latest news about Ukraine. I will use the web_search tool.
Action: web_search
Action Input: Ukraine latest news
Observation: You get result from using tool web_search: [list of search results with titles and URLs]
Thought: The search results show a lot about Sloviansk. I should read one of the articles to get more details.
...
and the loop continues until you have enough information to write the report. Do not directly write you thoughts just use this example for internal guidance on how to structure your thinking and tool usage. 
"""

FINAL_PROMPT = """
STOP. You have reached your limit. Do not use tools. 
Based ONLY on the info already gathered, write a detailed final report. 
You MUST use the 'write_report' tool to submit your detailed final report.
"""