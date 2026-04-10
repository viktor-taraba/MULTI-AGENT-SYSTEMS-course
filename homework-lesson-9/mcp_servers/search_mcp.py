import os, sys #to delete
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import trafilatura
import yfinance  as yf
import json
from fastmcp import FastMCP
from typing import List, Dict
from ddgs import DDGS
from config import (
    max_search_results, 
    max_url_content_length, 
    output_dir, 
    desired_keys_yfinance, 
    period_yfinance, 
    email_crossref_api
    )
import asyncio
import threading
import time
import requests

mcp_server = FastMCP(name="SearchMCP")

@mcp_server.tool
def web_search(query: str, max_search_results: int = max_search_results) -> str:
    """
    Search the web to find up-to-date information.
    Use this FIRST to find relevant URLs and basic summaries. Do not base your final answer solely on these short snippets.",

    Args:
        query (str): The search query or question to look up.

    Returns:
        str: A JSON-formatted string containing list of search results containing 'title', 'url', and 'snippet'.
    """
    processed_results: List[Dict[str, str]] = []

    try:
        raw_results = DDGS().text(query, max_results=max_search_results)
        if not raw_results:
            return json.dumps(processed_results)

        for item in raw_results:
            processed_results.append({
                "title": item.get("title", ""),
                "url": item.get("href", ""),
                "snippet": item.get("body", "")
            })

    except Exception as e:
        return f"Error during search for '{query}': {e}"

    return json.dumps(processed_results)

@mcp_server.tool
def find_articles_crossref(query: str, max_search_results: int = max_search_results, email_crossref_api: str = email_crossref_api) -> str:
    """
    Searches the Crossref database for scientific articles, journals, and conference papers.
    Use this tool when you need to find peer-reviewed research, metadata, or summaries 
    for specific academic topics or information from scientific articles on the specific topic.

    Args:
        query: A specific short search string containing keywords, topics, or paper titles 
               (e.g., "llm banking" or "dividend policy"). Do not use more than 2-3 words for one query.

    Returns:
        str: A json-formatted list of dictionaries containing 'title', 'abstract', 'doi', and 'year'.
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
                    
            return json.dumps(filtered_articles)
        else:
            return f"Error: {response.status_code}"
            
    except Exception as e:
        return f"An error occurred: {e}"

@mcp_server.tool
def stock_company_info(stock_ticker: str, result_type: str, desired_keys_yfinance: str = desired_keys_yfinance) -> str:
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
        str:  A JSON-formatted string containing the requested data. If an error occurs 
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

def run_mcp_server():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(
        mcp_server.run_async(transport="streamable-http", host="127.0.0.1", port=8901)
    )

server_thread = threading.Thread(target=run_mcp_server, daemon=True)
server_thread.start()
time.sleep(3)
print("✅ MCP Server 'ProjectTracker' running at http://127.0.0.1:8901/mcp")

"""
print("\n Testing tool call\n")
result = web_search("Latest news about space exploration")
print(result)
print("\n Tool call finished\n")

print("\n Testing resource\n")
result = get_output_dir("test")
print(result)
print("\n Test finished\n")
"""

from fastmcp import Client
import asyncio

async def test_mcp_server():
    async with Client("http://127.0.0.1:8901/mcp") as client:
        # 1. List available tools
        tools = await client.list_tools()
        print()
        print('-' * 50)
        print("Available Tools:")
        for t in tools: print(f"   - {t.name}: {(t.description or '')}")
        print()

        # 2. List available resources
        resources = await client.list_resources()
        print('-' * 50)
        print("Available Resources:")
        for r in resources: print(f"   - {r.uri}: {r.name}")
        print()


if __name__ == "__main__":
    asyncio.run(test_mcp_server())