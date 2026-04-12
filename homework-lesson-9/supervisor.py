from langchain_core.tools import tool
from acp_sdk.client import Client as ACPClient
from acp_sdk.models import Message, MessagePart
from config import ( 
    revision_counter_max,
    tool_preview_len,
    port_acp_server,
    port_report_mcp,
    udp_log_port
)
from langgraph.errors import GraphRecursionError
from langchain.agents.middleware.tool_call_limit import ToolCallLimitExceededError
import socket
import json
from fastmcp import Client as MCPClient

acp_address = f"http://127.0.0.1:{port_acp_server}"
mcp_report_address = f"http://127.0.0.1:{port_report_mcp}/mcp"

revision_counter = 0
global current_research_session

broadcast_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def cross_terminal_print(text, agent_name):
    """Prints locally, and if it's a sub-agent, broadcasts to the Supervisor terminal."""
    print(text) 
    if agent_name != "Supervisor":
        try:
            broadcast_sock.sendto(text.encode('utf-8'), ('127.0.0.1', udp_log_port))
        except Exception:
            pass

def print_tool_call(tool_name, tool_args, indent="", agent_name="Supervisor"):
    tool_args = tool_args[:tool_preview_len] + "..." if len(tool_args) > tool_preview_len else tool_args
    cross_terminal_print(f"{indent}🔧 Tool called -> {tool_name}({tool_args})", agent_name)

def print_agent_step(msg, agent_name="Supervisor"):
    """Parses a single LangChain message object and prints it in a clean format."""
    indent = "    " if agent_name != "Supervisor" else ""

    msg_type = getattr(msg, "type", None)
    msg_content = getattr(msg, "content", "")

    if msg_type == "ai":
        if msg_content and agent_name == "Supervisor":
            cross_terminal_print(f"\n{indent}🤖 Agent:\n{msg_content}", agent_name=agent_name)
        
        tool_calls = getattr(msg, "tool_calls", [])
        if tool_calls:
            for tool_call in tool_calls:
                if isinstance(tool_call, dict):
                    tool_name = tool_call.get("name")
                    tool_args = str(tool_call.get("args"))
                else:
                    tool_name = getattr(tool_call, "name", "Unknown")
                    tool_args = str(getattr(tool_call, "args", "{}"))
                if tool_name:
                    print_tool_call(tool_name,tool_args,indent=indent, agent_name=agent_name)

    elif msg_type == "tool":
        tool_name = getattr(msg, "name", "unknown_tool")
        content_str = str(msg_content)

        if tool_name in ["plan", "critique"]:
            try:
                parsed_json = json.loads(content_str)
                content_str = json.dumps(parsed_json, indent=2, ensure_ascii=False)
            except Exception:
                pass
        message_len = len(content_str) if tool_name in ["plan","research","critique"] else tool_preview_len 
        preview = content_str[:message_len] + "..." if len(content_str) > message_len else content_str

        if tool_name in ["plan","research","critique"]:

            cross_terminal_print(f"{indent}✅ Result ({tool_name}):", agent_name=agent_name)
            formatted_name = tool_name.replace("_", " ").title()
            lines = content_str.splitlines()
            if tool_name == "research":
                indented_content = "\n".join(f"{indent}│ {line}" for line in lines[:25])
                if len(lines) > 25:
                    indented_content += f"\n{indent}│ ... (25/{len(lines)} rows) ..."
            else:
                indented_content = "\n".join(f"{indent}│ {line}" for line in lines)
            cross_terminal_print(f"\n{indent}╭─── 📄 {formatted_name} {'─' * (40 - len(formatted_name))}", agent_name=agent_name)
            cross_terminal_print(indented_content, agent_name=agent_name)
            cross_terminal_print(f"{indent}╰{'─' * 46}\n", agent_name=agent_name)

        else:
            cross_terminal_print(f"{indent}✅ Result ({tool_name}): {preview}", agent_name=agent_name)

@tool
async def plan(request: str) -> str:
    """Create structured, step-by-step research plans from user requests.

    Usage:
    - Break down a question or topic into an actionable research strategy
    - Formulate specific search queries and determine the best data sources (web vs. internal)
    - Define the optimal structure and formatting for a final research report

    Input: Natural language research topic or request
    (e.g., 'Create a plan to research the market impact of solid-state batteries')
    """
    print(f"\n╭{'─'*30}\n│   [Supervisor → ACP → Planner]\n╰{'─'*30}")

    try:
        async with ACPClient(base_url=acp_address, headers={"Content-Type": "application/json"}) as client:
            run = await client.run_sync(
                agent="planner",
                input=[Message(role="user", parts=[MessagePart(content=request)])]
            )
            if not run.output:
                return "Error: The ACP Server encountered a fatal Python error and returned no output. Check the ACP Server terminal logs!"                
            return run.output[-1].parts[0].content
            
    except Exception as e:
        return f"Error: Could not communicate with ACP Planner. Details: {e}"

@tool
async def research(plan: str) -> str:
    """Execute deep-dive research and generate a comprehensive Markdown report.

    Usage:
    - Execute a structured research plan or answer a complex, multi-step query
    - Gather detailed facts, statistics, and deep context from full articles (not just search snippets)
    - Search across external web sources, internal databases, financial data, or academic articles
    - Find current information from the web
    - Look up company policies, contacts, or OKRs
    - Get summaries of internal documentation
    - Compile gathered findings into a final, well-formatted Markdown report

    Input: A specific research query or a detailed research plan generated by the Planner.
    (e.g., 'Execute this research plan: Goal is to analyze TSLA financials. Queries: ...')
    """
    print(f"\n╭{'─'*30}\n│   [Supervisor → ACP → Researcher]\n╰{'─'*30}")

    try:
        async with ACPClient(base_url=acp_address, headers={"Content-Type": "application/json"}) as client:
            run = await client.run_sync(
                agent="researcher",
                input=[Message(role="user", parts=[MessagePart(content=plan)])]
            )
            if not run.output:
                return "Error: The ACP Server encountered a fatal Python error and returned no output. Check the ACP Server terminal logs!"                
            return run.output[-1].parts[0].content

    except Exception as e:
        return f"Error: Could not communicate with ACP Researcher. Details: {e}"

@tool
async def critique(findings: str) -> str:
    """Independently review, fact-check, and evaluate a drafted research report.

    Usage:
    - Verify if the findings in a drafted report are accurate, up-to-date, and supported by sources
    - Check if the research fully covers the user's original request (completeness)
    - Assess the logical structure of the drafted text
    - Get a final verdict (APPROVE or REVISE) along with specific actionable revision requests

    Input: A string containing BOTH the original user request and the drafted research report.
    (e.g., 'Original request: [Topic]. Draft report: [Markdown text...]')
    """
    print(f"\n╭{'─'*30}\n│   [Supervisor → ACP → Critic]\n╰{'─'*30}")

    global revision_counter
    revision_counter += 1

    if revision_counter > revision_counter_max:
        print(f"\n⚠️ Critic Tool: Reached maximum revisions ({revision_counter}). Forcing APPROVE without calling agent.")
        import json
        mock_critique = {
            "verdict": "APPROVE",
            "is_fresh": True,
            "is_complete": True,
            "is_well_structured": True,
            "strengths": ["Achieved max number of iterations. Report is approved"],
            "gaps": ["No gaps"],
            "revision_requests": ["Achieved max number of iterations. Report is approved, it is the final version, save it."]
        }
        return f"--- CRITIQUE ROUND {revision_counter}/{revision_counter_max} ---\n" + json.dumps(mock_critique, indent=2)

    try:
        async with ACPClient(base_url=acp_address, headers={"Content-Type": "application/json"}) as client:
            run = await client.run_sync(
                agent="critic",
                input=[Message(role="user", parts=[MessagePart(content=findings)])]
            )
            if not run.output:
                return "Error: The ACP Server encountered a fatal Python error and returned no output. Check the ACP Server terminal logs!"                
            critique_result = run.output[-1].parts[0].content

            return f"--- CRITIQUE ROUND {revision_counter}/{revision_counter_max} ---\n" + critique_result
            
    except Exception as e:
        return f"--- CRITIQUE ROUND {revision_counter}/{revision_counter_max} ---\n Error: Could not communicate with ACP Critic. Details: {e}"

@tool
async def save_report(filename: str, content: str) -> str:
    """
    Saves the final Markdown report to the local disk.
    Use this tool ONLY when the report is completely finished and you are ready to give the final answer.
    
    Args:
        filename (str): The name of the file to save (e.g., 'report.md').
        content (str): The full Markdown text of the report.
        
    Returns:
        str: A confirmation message with the full path to the saved file, or an error message.
    """

    print(f"\n╭{'─'*30}\n│   [Supervisor → MCP → save_report]\n╰{'─'*30}")
    
    try:
        async with MCPClient(mcp_report_address) as client:
            result = await client.call_tool("save_report", {"filename": filename, "content": content})
            
            if hasattr(result, "content") and isinstance(result.content, list):
                extracted_texts = [
                    item.text for item in result.content 
                    if getattr(item, "type", "") == "text"
                ]
                return "\n".join(extracted_texts)
            return str(result)
            
    except Exception as e:
        return f"Error: Could not communicate with ReportMCP. Details: {e}"

# TO DELETE
# test runs for supervisor
import asyncio
from langchain.agents import create_agent

from config import (
    SUPERVISOR_PROMPT, 
    supervisor_model_name, 
    tool_preview_len
    )
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv
load_dotenv()

# ============================================================
# 1. Create the Local Supervisor Agent
# ============================================================

supervisor = create_agent(
                model=supervisor_model_name,
                tools=[plan, research, critique, save_report],
                system_prompt=SUPERVISOR_PROMPT,
                checkpointer=InMemorySaver())

# ============================================================
# 2. Async Test Function
# ============================================================
class LogReceiver(asyncio.DatagramProtocol):
    def datagram_received(self, data, addr):
        print(data.decode('utf-8'))

async def run_and_print_supervisor(query: str):
    loop = asyncio.get_running_loop()
    
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: LogReceiver(),
        local_addr=('127.0.0.1', udp_log_port)
    )

    print(f"🚀 Starting Supervisor test...\nQuery: '{query}'\n" + "="*60)
    try:
        config = {"configurable": {"thread_id": "test_thread_1"}} 
        async for step in supervisor.astream({"messages": [("user", query)]}, config):

            for node_name, update in step.items():
                if isinstance(update, dict) and "messages" in update:
                    messages = update["messages"]
                    if not isinstance(messages, list):
                        messages = [messages]
                    for msg in messages:
                        print_agent_step(msg, agent_name="Supervisor")
        
    except Exception as e:
        print(f"\n❌ Supervisor encountered an error: {e}")
    finally:
        transport.close()

# ============================================================
# 3. Execution Block
# ============================================================
if __name__ == "__main__":
    test_query = "What is the difference between the BM25 algorithm and TF-IDF? Explain how they calculate relevance."
    asyncio.run(run_and_print_supervisor(test_query))

# TO DO:
# додати обробку для випадку з помилкою при обмеженні к-ті виклику тулів та суттєво скоротити ліміт тулів для тестування
# перенесети скрипт звідси в main
# HITL 
# додати один приклад нового аутпуту в папку output
# оформити README, почистити зайві коменти
# додати пару тулів по РВІ та звіти в папці, і додати це все до проекту