import os, sys #to delete
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastmcp import FastMCP
import asyncio
import threading
import json
from config import output_dir

from pathlib import Path
OUTPUT_PATH = Path(r"C:\Users\Viktor\source\repos\MULTI-AGENT-SYSTEMS-course\homework-lesson-9\output")

mcp_server = FastMCP(name="ReportMCP")

@mcp_server.resource("resource://output-dir/{folder}")
def get_output_dir(folder: str = "default") -> str:
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

@mcp_server.tool
def save_report(filename: str, content: str, output_dir: str = output_dir) -> str:
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

def run_mcp_server():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(
        mcp_server.run_async(transport="streamable-http", host="127.0.0.1", port=8902)
    )

server_thread = threading.Thread(target=run_mcp_server, daemon=True)
server_thread.start()
print("✅ MCP Server 'ProjectTracker' running at http://127.0.0.1:8902/mcp")


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