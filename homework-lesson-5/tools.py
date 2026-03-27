import os
import trafilatura
import yfinance  as yf
import json
import io
import requests
import logging
import re
from ddgs import DDGS
from config import (
    max_search_results, 
    max_url_content_length, 
    output_dir, 
    desired_keys_yfinance, 
    period_yfinance, 
    email_crossref_api,
    RAG_topics,
    rerank_top_n
    )
from typing import List, Dict
from pypdf import PdfReader
from retriever import get_retriever

knowledge_search_tool_schema = {
    "type": "function",
    "name": "knowledge_search",
    "description": f"Search the local knowledge database which have information about following topucs: {RAG_topics}. Returns top {rerank_top_n} releveant search results. Automatically filters out irrelevant noise via reranking.",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search query or question to look up., e.g. 'DAX measures' or 'LLM monitoring'"
            }
        },
        "required": ["query"]
    }
}

def knowledge_search(query: str) -> str:
    """Search the local knowledge base using hybrid retrieval + reranking."""
    try:
        results = get_retriever(query)
        if not results:
            return "No documents found for this query. Try rephrasing."
        else:
            return results
    except Exception as e:
        return f"Error searching local knowledge base. Details: {e}."

web_search_tool_schema = {
    "type": "function",
    "name": "web_search",
    "description": "Search the web to find up-to-date information. Returns list of search results containing 'title', 'url', and 'snippet'. Use this FIRST to find relevant URLs and basic summaries. Do not base your final answer solely on these short snippets.",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search query or question to look up., e.g. 'Dynamic pricing models'"
            }
        },
        "required": ["query"]
    }
}

def web_search(query: str) -> str:
    """
    Search the web to find up-to-date information.
    Use this FIRST to find relevant URLs and basic summaries. Do not base your final answer solely on these short snippets.",

    Args:
        query (str): The search query or question to look up.

    Returns:
        List[Dict[str, str]]: A list of search results containing 'title', 'url', and 'snippet'.
    """
    processed_results: List[Dict[str, str]] = []

    try:
        raw_results = DDGS().text(query, max_results=max_search_results)
        if not raw_results:
            return processed_results

        for item in raw_results:
            processed_results.append({
                "title": item.get("title", ""),
                "url": item.get("href", ""),
                "snippet": item.get("body", "")
            })

    except Exception as e:
        return f"Error during search for '{query}': {e}"

    return json.dumps(processed_results)

# read_url_pdf will be used at read_url function, not as a separate tool for llm agent
def read_url_pdf(url: str):
    """
    Fetches a PDF from a URL and extracts its text in-memory.
    """
    try:
        # Mute pypdf's warnings about broken pdfs so they don't flood the agent's console
        logging.getLogger("pypdf").setLevel(logging.ERROR)

        response = requests.get(url, timeout=5)
        response.raise_for_status()
        content_type = response.headers.get('Content-Type', '').lower()
        if 'application/pdf' not in content_type:
            return f"Error: The server blocked the download or requires a subscription. It returned an HTML page instead of a PDF (Content-Type: {content_type}).\
                     DO NOT try to read this URL again. Move on and use the other information you have gathered."

        # Load the raw downloaded bytes into a virtual memory file
        pdf_bytes = io.BytesIO(response.content)
        reader = PdfReader(pdf_bytes)

        full_text = []
        for i, page in enumerate(reader.pages):
            page_text = page.extract_text()
            
            if page_text:
                full_text.append(f"--- Page {i + 1} ---\n{page_text}")
            if i > max_search_results:
                break

        final_text = "\n\n".join(full_text)
        
        return final_text

    except Exception as e:
        return f"Error extracting PDF from {url}. Details: {e}. DO NOT try to read this URL again. Move on and use the other information you have gathered."

read_url_tool_schema = {
    "type": "function",
    "name": "read_url",
    "description": "Fetches and extracts the main text content from a given URL. Use this AFTER a web search to read the full, in-depth content of\
    a webpage. Essential for gathering detailed facts, examples, and deep context for your final report. This function acts as a tool for an LLM\
    agent to read the full content of a webpage. It deliberately truncates the output to prevent blowing up the LLM's context window (context engineering). It also catches errors so the agent can recover.",
    "parameters": {
        "type": "object",
        "properties": {
            "url": {
                "type": "string",
                "description": "The URL of the webpage to read., e.g. 'https://...'"
            }
        },
        "required": ["url"]
    }
}

def read_url(url: str) -> str:
    """
    Fetches and extracts the main text content from a given URL.
    Use this AFTER a web search to read the full, in-depth content of a webpage.
    Essential for gathering detailed facts, examples, and deep context for your final report.
    This function acts as a tool for an LLM agent to read the full content of a webpage.
    It deliberately truncates the output to prevent blowing up the LLM's context window
    (context engineering). It also catches errors so the agent can recover.

    Args:
        url (str): The URL of the webpage to read, , e.g. 'https://...'.

    Returns:
        str: The extracted plain text from the webpage, or an error message if extraction fails.
    """

    try:
        if url.endswith('.pdf'):
            text = read_url_pdf(url)

        else: 
            downloaded = trafilatura.fetch_url(url)
            if downloaded is None:
                return f"Error: Unable to fetch content from '{url}'. The page might be inaccessible, invalid, or blocking automated requests."
            text = trafilatura.extract(downloaded)

            if not text:
                return f"Error: Fetched '{url}' successfully, but could not extract meaningful text. The page might rely heavily on JavaScript."

        if len(text) > max_url_content_length:
            text = text[:max_url_content_length]
            return text

        return text

    except Exception as e:
        return f"An unexpected error occurred while reading '{url}': {str(e)}. DO NOT try to read this URL again. Move on and use the other information you have gathered."

stock_company_info_tool_schema = {
    "type": "function",
    "name": "stock_company_info",
    "description": "Fetches financial data or company profile information for a given ticker (stock, ETF). Use this tool ONLY if financial data\
    (stock prices, company financials) or general information about a publicly traded company or about ETF or other financial instrument which a\
    ticker is needed, AND the specific stock ticker symbol is known. This tool queries the Yahoo Finance API to retrieve either 3 months of daily\
    historical price data or a filtered dictionary of general company information. The output is returned as a JSON-formatted string.",
    "parameters": {
        "type": "object",
        "properties": {
            "stock_ticker": {
                "type": "string",
                "description": "The standard stock ticker symbol to query (e.g., MSFT, AAPL)"
            },
            "result_type": {
                "type": "string",
                "description": "Determines the type of data to return. Use 'stock_data' to retrieve the last 3 months of historical market data.\
                Use 'info' (or any other string) to retrieve the companys general profile."
            }
        },
        "required": ["stock_ticker", "result_type"]
    }
}

def stock_company_info(stock_ticker: str, result_type: str) -> str:
    """
    Fetches financial data or company profile information for a given ticker (stock, ETF).

    Use this tool ONLY if financial data (stock prices, company financials) or 
    general information about a publicly traded company or about ETF or other financial instrument which a ticker
    is needed, AND the specific stock ticker symbol is known.

    This tool queries the Yahoo Finance API to retrieve either 3 months of daily 
    historical price data or a filtered dictionary of general company information. 
    The output is returned as a JSON-formatted string.

    Args:
        stock_ticker (str): The standard stock ticker symbol to query (e.g., "MSFT", "AAPL").
        result_type (str): Determines the type of data to return. 
            - Use "stock_data" to retrieve the last 3 months of historical market data.
            - Use "info" (or any other string) to retrieve the company's general profile.

    Returns:
        json: A JSON-formatted string containing the requested data. If an error occurs 
              during the API call, it returns a string detailing the exception.
    """

    try:
        company = yf.Ticker(stock_ticker)

        if result_type == "stock_data":
            df = company.history(period=period_yfinance)
            df["Date"] = df.index.date

            return df.to_json(orient='records', lines=True)
        
        else:
            filtered_info = {key: company.info.get(key) for key in desired_keys_yfinance}

            return json.dumps(filtered_info)

    except Exception as e:
        return f"Error using function stock_info. Details: {e}"

find_articles_crossref_tool_schema = {
    "type": "function",
    "name": "find_articles_crossref",
    "description": "Searches the Crossref database for scientific articles, journals, and conference papers. Use this tool when you need to find\
    peer-reviewed research, metadata, or summaries for specific academic topics or information from scientific articles on the specific topic.",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "A specific short search string containing keywords, topics, or paper titles (e.g., 'llm banking' or 'dividend policy').\
                Do not use more than 2-3 words for one query."
            }
        },
        "required": ["query"]
    }
}

def find_articles_crossref(query: str) -> str:
    """
    Searches the Crossref database for scientific articles, journals, and conference papers.
    Use this tool when you need to find peer-reviewed research, metadata, or summaries 
    for specific academic topics or information from scientific articles on the specific topic.

    Args:
        query: A specific short search string containing keywords, topics, or paper titles 
               (e.g., "llm banking" or "dividend policy"). Do not use more than 2-3 words for one query.

    Returns:
        A list of dictionaries containing 'title', 'abstract', 'doi', and 'year'.
        Only records that contain a valid summary (abstract) are returned. 
        Returns an error string if the API call fails.
    """

    # We request more than the limit (limit * 2) because many records in Crossref lack abstracts; this increases the chance of hitting target.
    url = f"https://api.crossref.org/works?query={query.replace(' ', '+')}&rows={max_search_results * 2}"
    headers = {"User-Agent": f"ResearchScript/1.0 (mailto:{email_crossref_api})"}
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            items = response.json()['message']['items']

            filtered_articles = []
            for i in items:
                abstract = i.get('abstract')
                
                if abstract and len(abstract.strip()) > 0:
                    clean_abstract = re.sub(r'<[^>]+>', '', abstract)
                    
                    filtered_articles.append({
                        "title": i.get('title', ['No Title'])[0],
                        "abstract": clean_abstract.strip(),
                        "doi": i.get('DOI'),
                        "year": i.get('created', {}).get('date-parts', [[None]])[0][0]
                    })
                
                if len(filtered_articles) >= max_search_results:
                    break
                    
            return filtered_articles
        else:
            return f"Error: {response.status_code}"
            
    except Exception as e:
        return f"An error occurred: {e}"

write_report_tool_schema = {
    "type": "function",
    "name": "write_report",
    "description": "Saves the final Markdown report to the local disk. Use this tool ONLY when the report is completely finished and you are ready to give the final answer.",
    "parameters": {
        "type": "object",
        "properties": {
            "filename": {
                "type": "string",
                "description": "The name of the file to save (e.g., 'report.md')."
            },
            "content": {
                "type": "string",
                "description": "The full Markdown text of the report."
            }
        },
        "required": ["filename","content"]
    }
}

def write_report(filename: str, content: str) -> str:
    """
    Saves the final Markdown report to the local disk.
    Use this tool ONLY when the report is completely finished and you are ready to give the final answer.
    
    Args:
        filename (str): The name of the file to save (e.g., 'report.md').
        content (str): The full Markdown text of the report.
        
    Returns:
        str: A confirmation message with the full path to the saved file, or an error message.
    """
    
    try:
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
           
        return f"Success: Report successfully saved to {os.path.abspath(filepath)}"
        
    except Exception as e:
        return f"Error: Could not save the report. Details: {e}"

tool_registry = {
    "web_search": web_search, 
    "read_url": read_url, 
    "knowledge_search": knowledge_search,
    "write_report": write_report, 
    "stock_company_info": stock_company_info,
    "find_articles_crossref": find_articles_crossref}

tools = [
    web_search_tool_schema, 
    read_url_tool_schema, 
    knowledge_search_tool_schema,
    write_report_tool_schema, 
    stock_company_info_tool_schema, 
    find_articles_crossref_tool_schema
    ]
