from typing import List, Dict
from ddgs import DDGS
import json
import sys
import os
import trafilatura

def write_report(filename: str, content: str) -> str:
    pass

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
            },
            "max_results": {
                "type": "integer",
                "description": "The maximum number of search results to return. Default is 5'"
            }
        },
        "required": ["query"]
    }
}

def web_search(query: str) -> list[dict]:
    """
    Search the web to find up-to-date information.

    Args:
        query (str): The search query or question to look up.

    Returns:
        List[Dict[str, str]]: A list of search results containing 'title', 'url', and 'snippet'.
    """
    processed_results: List[Dict[str, str]] = []

    try:
        # Cap the maximum results to 10 to prevent excessive API calls or token usage
        max_results = 10

        # Use DDGS to fetch search results
        raw_results = DDGS().text(query, max_results=max_results)

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
        #prevent the agent from crashing in case of network or rate limit issues
        return f"Error during search for '{query}': {e}"

    return processed_results

read_url_tool_schema = {
    "type": "function",
    "name": "read_url",
    "description": "Fetches and extracts the main text content from a given URL. Use this AFTER a web search to read the full, in-depth content of a webpage. Essential for gathering detailed facts, examples, and deep context for your final report.",
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

    This function acts as a tool for an LLM agent to read the full content of a webpage.
    It deliberately truncates the output to prevent blowing up the LLM's context window
    (context engineering). It also catches errors so the agent can recover.

    Args:
        url (str): The URL of the webpage to read.

    Returns:
        str: The extracted plain text from the webpage, or an error message if extraction fails.
    """
    # The maximum number of characters to return
    max_chars = 10000

    try:
        # fetch_url handles the HTTP request. It returns None if the request fails
        # (e.g., 404, timeout, or blocked by the server).
        downloaded = trafilatura.fetch_url(url)
        # !!!!! ось тут переробити, треба точни код помилки (а чи треба?)
        if downloaded is None:
            return f"Error: Unable to fetch content from '{url}'. The page might be inaccessible, invalid, or blocking automated requests."

        # extract parses the HTML and isolates the main article text.
        text = trafilatura.extract(downloaded)

        # Sometimes a page is fetched successfully, but contains no extractable text
        # (e.g., heavy client-side JavaScript rendering or purely visual pages).
        if not text:
            return f"Error: Fetched '{url}' successfully, but could not extract meaningful text. The page might rely heavily on JavaScript."

        # Context Engineering: Truncate the text if it exceeds the max_chars limit.
        if len(text) > max_chars:
            text = text[:max_chars]
            return text

        return text

    except Exception as e:
        # Catch-all for unexpected exceptions to prevent the entire agent process from crashing.
        return f"An unexpected error occurred while reading '{url}': {str(e)}"