from langchain_core.tools import tool
from typing import List, Dict
from ddgs import DDGS
import json
import sys
import os
import trafilatura
from config import max_search_results, max_url_content_length, output_dir

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
        #prevent the agent from crashing in case of network or rate limit issues
        return f"Error during search for '{query}': {e}"

    return processed_results

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
        # fetch_url handles the HTTP request. It returns None if the request fails
        # (e.g., 404, timeout, or blocked by the server).
        downloaded = trafilatura.fetch_url(url)
        if downloaded is None:
            return f"Error: Unable to fetch content from '{url}'. The page might be inaccessible, invalid, or blocking automated requests."

        # extract parses the HTML and isolates the main article text.
        text = trafilatura.extract(downloaded)

        # Sometimes a page is fetched successfully, but contains no extractable text
        # (e.g., heavy client-side JavaScript rendering or purely visual pages).
        if not text:
            return f"Error: Fetched '{url}' successfully, but could not extract meaningful text. The page might rely heavily on JavaScript."

        # Context Engineering: Truncate the text if it exceeds the max_chars limit.
        if len(text) > max_url_content_length:
            text = text[:max_url_content_length]
            return text

        return text

    except Exception as e:
        # Catch-all for unexpected exceptions to prevent the entire agent process from crashing.
        return f"An unexpected error occurred while reading '{url}': {str(e)}"