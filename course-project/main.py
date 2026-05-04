from langfuse.langchain import CallbackHandler
from langgraph.types import Command
from langgraph.errors import GraphInterrupt
from dotenv import load_dotenv
from langfuse import get_client
from datetime import datetime
from config import (
    tool_preview_len,
    recursion_limit
    )
from tools import tool_registry
from graph import dev_team_app
import json
import uuid
load_dotenv()

# додати тести по тулах (для кожного агента окремо) (все через deepeval)
# для оціночного плану запиту покращити форматування аутпуту
# додати до RAG відео та документ по оптимізації запитів
# Get_Sample_Rows: Accepts a table_name and returns the top 3–5 rows. This is crucial for agents to understand data formatting (e.g., are dates stored as YYYY-MM-DD or unix timestamps? Are strings lowercase?).

# подивитися як отримати фактичний план запиту, а не лише оціночнийs

langfuse = get_client()
langfuse_handler = CallbackHandler()

session_id = f"{datetime.now().isoformat()}-course-project-{uuid.uuid4().hex[:8]}"
user_id="viktor_hw_12"
tags=["course-project", "multi-agent"]

config = {"recursion_limit": recursion_limit,
    "callbacks": [langfuse_handler],
    "configurable": {
        "thread_id": f"session_{uuid.uuid4().hex[:8]}" 
    },
    "metadata": {
            "langfuse_user_id": user_id,
            "langfuse_session_id": session_id,
            "langfuse_tags": tags
        }}

def format_data(data, level=0):
    """helper function to format json schema output"""
    lines = []
    ind = "  " * level

    if isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, str) and '\n' in v:
                lines.append(f"{ind}{k}:")
                for line in v.splitlines():
                    lines.append(f"{ind}  {line}")
            elif isinstance(v, (dict, list)):
                lines.append(f"{ind}{k}:")
                lines.extend(format_data(v, level + 1))
            else:
                lines.append(f"{ind}{k}: {v}")

    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                lines.extend(format_data(item, level + 1))
            elif isinstance(item, str) and '\n' in item:
                lines.append(f"{ind}-")
                for line in item.splitlines():
                    lines.append(f"{ind}  {line}")
            else:
                lines.append(f"{ind}- {item}")
    return lines

def print_tool_call(tool_name, tool_args, indent=""):
    """Helper function for printing tool calls"""

    tool_args = tool_args[:tool_preview_len] + "..." if len(tool_args) > tool_preview_len else tool_args
    print(f"{indent}🔧 Tool called -> {tool_name}({tool_args})")

    tool_name = tool_registry.get(tool_name)
    if tool_name is None:
        print(f"{indent}❌ Unknown tool: {tool_name}")

def print_agent_step(msg):
    """Parses a single LangChain message object and prints it in a clean format."""
    indent = "    "

    msg_type = getattr(msg, "type", None)
    msg_content = getattr(msg, "content", "")

    content_str = str(msg_content).strip()
    if content_str.startswith("{") or content_str.startswith("["):
        try:
            parsed_json = json.loads(content_str)
            formatted_lines = format_data(parsed_json)
            content_str = "\n".join(formatted_lines)
        except json.JSONDecodeError:
            pass

    if msg_type == "ai":
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
                    print_tool_call(tool_name,tool_args,indent=indent)

        if content_str:
            print(f"{indent}🤖 Agent Output:")
            lines = content_str.splitlines()
            indented_content = "\n".join(f"{indent}│ {line}" for line in lines)
            print(indented_content)
            print(f"{indent}╰{'─' * 46}\n")

    elif msg_type == "tool":
        tool_name = getattr(msg, "name", "unknown_tool")
        
        print(f"{indent}✅ Result ({tool_name}):")
        formatted_name = tool_name.replace("_", " ").title()
        lines = content_str.splitlines()
        indented_content = "\n".join(f"{indent}│ {line}" for line in lines)
        print(f"\n{indent}╭─── 📄 {formatted_name} {'─' * (40 - len(formatted_name))}")
        print(indented_content)
        print(f"{indent}╰{'─' * 46}\n")

def main():
    print("SQL / DWH Assistant")
    print("type 'exit' or 'quit' to quit")
    print("-" * 100)

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        try:
            current_input = {"messages": [{"role": "user", "content": user_input}]}

            while True:
                try:
                    # Run the graph until it finishes or hits an interrupt
                    for event in dev_team_app.stream(current_input, config=config, subgraphs=True):
                        namespace, step = event
                        
                        for node_name, update in step.items():
                            # usual agent messages
                            if isinstance(update, dict) and "messages" in update:
                                for message in update.get("messages", []):
                                    print_agent_step(message)

                except GraphInterrupt:
                    pass
            
                # Check the state to see if it paused
                state = dev_team_app.get_state(config)
                # If state.next has items, the graph is paused at our human_approval_gate
                if state.next:
                    print(f"\n{'=' * 60}")
                    print(f" ⏸️  ACTION REQUIRES APPROVAL (HITL)")
                    print(f"{'=' * 60}")
                    
                    interrupt_prompt = "Please review. Type 'APPROVED' to accept, or provide feedback to revise."
                    if state.tasks and state.tasks[0].interrupts:
                        interrupt_prompt = state.tasks[0].interrupts[0].value
                    print(f"\nSystem: {interrupt_prompt}")
                    human_feedback = input("Your Feedback: ").strip()
                    
                    current_input = Command(resume=human_feedback)
                else:
                    # state.next is empty, meaning the graph reached __end__ successfully
                    break

        except Exception as e:
            print(f"\n❌ An error occurred: {e}. Try again or type 'continue'")

if __name__ == "__main__":
    main()