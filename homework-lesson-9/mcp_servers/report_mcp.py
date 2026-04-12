from fastmcp import FastMCP
import json
import os, sys 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import (
    output_dir, 
    port_report_mcp, 
    output_path)
from pathlib import Path

OUTPUT_PATH = Path(output_path)

base_port = f"http://127.0.0.1:{port_report_mcp}/mcp"
mcp_server = FastMCP(name="ReportMCP")

@mcp_server.resource("resource://output-dir")
def get_output_dir() -> str:
    """
    Returns the directory path and a list of saved reports.
    """
    try:
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

if __name__ == "__main__":
    print(f"✅ Starting MCP Server 'ReportMCP' on {base_port}")
    try:
        mcp_server.run(transport="streamable-http", host="127.0.0.1", port=port_report_mcp)
    except KeyboardInterrupt:
        print(f"🛑 MCP Server 'ReportMCP' {base_port} stopped")