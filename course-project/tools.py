from langchain_core.tools import tool
import os
import trafilatura
import json
import io
import requests
import logging
from ddgs import DDGS
from config import (
    max_search_results, 
    max_url_content_length,
    server,
    database
    )
from typing import List, Dict
from pypdf import PdfReader
from retriever import get_retriever

import pyodbc

#@tool
def execute_sql_query(query: str) -> str:
    """
    Executes a SQL query against a SQL Server database and returns the results.
    Use this tool when you need to retrieve data from the database, for example, information about departments (Department).
    
    Args:
        query (str): Formatted SQL query to execute (e.g., "SELECT * FROM [HumanResources].[Department]").
        
    Returns:
        str: Query results in JSON format (list of dictionaries) or an error message.
    """

    connection_string = f'''
        DRIVER={{ODBC Driver 17 for SQL Server}};
        SERVER={server};
        DATABASE={database};
        Trusted_Connection=yes;
    '''
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute(query)
        
        # Check if the query returns data (SELECT statement)
        if cursor.description:
            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()
            result_data = [dict(zip(columns, row)) for row in rows]
            return json.dumps(result_data, default=str)
        else:
            # If it's an INSERT/UPDATE/DELETE statement
            conn.commit()
            return json.dumps({"status": "success", "message": "Query executed successfully. No rows returned."})
            
    except pyodbc.Error as e:
        return json.dumps({"status": "error", "error_message": str(e)})
        
    finally:
        if 'conn' in locals():
            conn.close()

@tool
def knowledge_search(query: str) -> str:
    """
    Search the local knowledge database which has information about the following topics: large language models, langchain, RAG, Power BI, DAX documentations for Power BI, Power BI and agentic development, changes in Power BI with he new version.
    Returns top releveant search results.
    Automatically filters out irrelevant noise via reranking.

    Args:
        query (str): Search query or question to look up, e.g. 'DAX measures' or 'LLM monitoring'.

    Returns:
        str: Most relevant document fragments (Content + Source).
    """
    try:
        results = get_retriever(query)
        if not results:
            return "No documents found for this query. Try rephrasing."
        else:
            return results
    except Exception as e:
        return f"Error searching local knowledge base. Details: {e}."

@tool
def web_search(query: str) -> str:
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

tool_registry = {
    "web_search": web_search, 
    "read_url": read_url, 
    "knowledge_search": knowledge_search
    }
    #"execute_sql_query": execute_sql_query}

tools = [
    web_search, 
    read_url, 
    knowledge_search]
    #execute_sql_query]

agent_query = """
    SELECT TOP (5) [DepartmentID], [Name], [GroupName], [ModifiedDate]
    FROM [AdventureWorks2022].[HumanResources].[Department]
"""
    
agent_response = execute_sql_query(query=agent_query)
print(agent_response)