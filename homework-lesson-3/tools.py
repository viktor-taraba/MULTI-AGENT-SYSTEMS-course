from langchain_core.tools import tool
import os
import trafilatura
import yfinance  as yf
import pandas as pd
import json
import io
import requests
import logging
import re
from ddgs import DDGS
from config import max_search_results, max_url_content_length, output_dir, desired_keys_yfinance, period_yfinance, email_crossref_api
from typing import List, Dict
from pypdf import PdfReader

@tool
def web_search(query: str) -> list[dict]:
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

        # Return an empty list if no results are found
        if not raw_results:
            return processed_results

        # Map DDGS keys (href, body) to LLM-friendly keys (title, url, snippet)
        for item in raw_results:
            processed_results.append({
                "title": item.get("title", ""),
                "url": item.get("href", ""),
                "snippet": item.get("body", "")
            })

    except Exception as e:
        return f"Error during search for '{query}': {e}"

    return processed_results

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

        # Extract the text page by page
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

@tool
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
        # for pdf files
        if url.endswith('.pdf'):
            text = read_url_pdf(url)

        else: 
            # fetch_url handles the HTTP request. It returns None if the request fails (e.g., 404, timeout, or blocked by the server).
            downloaded = trafilatura.fetch_url(url)
            if downloaded is None:
                return f"Error: Unable to fetch content from '{url}'. The page might be inaccessible, invalid, or blocking automated requests."

            # extract parses the HTML and isolates the main article text.
            text = trafilatura.extract(downloaded)

            # Sometimes a page is fetched successfully, but contains no extractable text (e.g., heavy client-side JavaScript rendering or purely visual pages).
            if not text:
                return f"Error: Fetched '{url}' successfully, but could not extract meaningful text. The page might rely heavily on JavaScript."

        # Context Engineering: Truncate the text if it exceeds the max_chars limit.
        if len(text) > max_url_content_length:
            text = text[:max_url_content_length]
            return text

        return text

    except Exception as e:
        return f"An unexpected error occurred while reading '{url}': {str(e)}. DO NOT try to read this URL again. Move on and use the other information you have gathered."

@tool
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

        # stock prices, dividends etc
        if result_type == "stock_data":
            df = company.history(period=period_yfinance)
            df["Date"] = df.index.date

            return df.to_json(orient='records', lines=True)
        
        # company info and last financial statements data otherwise
        else:
            filtered_info = {key: company.info.get(key) for key in desired_keys_yfinance}

            return json.dumps(filtered_info)

    except Exception as e:
        return f"Error using function stock_info. Details: {e}"

@tool
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
                
                # Condition: Only include if abstract is present and not whitespace
                if abstract and len(abstract.strip()) > 0:
                    # Remove XML/JATS tags from the abstract text
                    clean_abstract = re.sub(r'<[^>]+>', '', abstract)
                    
                    filtered_articles.append({
                        "title": i.get('title', ['No Title'])[0],
                        "abstract": clean_abstract.strip(),
                        "doi": i.get('DOI'),
                        "year": i.get('created', {}).get('date-parts', [[None]])[0][0]
                    })
                
                # Stop once we have reached the limit
                if len(filtered_articles) >= max_search_results:
                    break
                    
            return filtered_articles
        else:
            return f"Error: {response.status_code}"
            
    except Exception as e:
        return f"An error occurred: {e}"

@tool
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