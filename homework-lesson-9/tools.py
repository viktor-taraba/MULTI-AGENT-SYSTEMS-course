from langchain_core.tools import tool
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
    email_crossref_api
    )
from typing import List, Dict
from pypdf import PdfReader
from retriever import get_retriever

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