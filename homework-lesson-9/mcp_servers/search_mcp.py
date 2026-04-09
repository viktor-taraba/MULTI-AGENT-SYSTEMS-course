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

from pathlib import Path
OUTPUT_PATH = Path(r"C:\Users\Viktor\source\repos\MULTI-AGENT-SYSTEMS-course\homework-lesson-9\output")

mcp_server = FastMCP(name="SearchMCP")

@mcp_server.resource("resource://output-dir//{output_dir}")
def get_output_dir(output_dir: str = output_dir) -> str:
    """
    Returns the directory path and a list of saved reports.
    """
    try:
        # Get all files in the output directory
        saved_reports = [file.name for file in OUTPUT_PATH.iterdir() if file.is_file()]
    except Exception as e:
        return json.dumps({"error": f"Failed to read directory: {str(e)}"})

    return json.dumps({
        "directory_path": str(OUTPUT_PATH.absolute()),
        "saved_reports": saved_reports,
        "total_files": len(saved_reports)
    }, indent=2)

print("✅ Resources: resource://output-dir")

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

print("✅ Tools")

def run_mcp_server():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(
        mcp_server.run_async(transport="streamable-http", host="127.0.0.1", port=8902)
    )

server_thread = threading.Thread(target=run_mcp_server, daemon=True)
server_thread.start()
time.sleep(3)
print("✅ MCP Server 'ProjectTracker' running at http://127.0.0.1:8902/mcp")


print("\n Testing tool call\n")
result = web_search("Latest news about space exploration")
print(result)
print("\n Tool call finished\n")

print("\n Testing resource\n")
result = get_output_dir("test")
print(result)
print("\n Test finished\n")


from fastmcp import Client
import asyncio

async def test_mcp_server():
    async with Client("http://127.0.0.1:8902/mcp") as client:
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