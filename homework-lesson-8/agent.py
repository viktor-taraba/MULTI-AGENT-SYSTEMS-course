from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
from tools import tools, tool_registry
from config import (
    FINAL_PROMPT, 
    SYSTEM_PROMPT,
    max_iterations, 
    model_name
)
import json
from dotenv import load_dotenv
load_dotenv()

def print_tool_call(tool_name, tool_args):
    tool_args = tool_args[:100] + "..." if len(tool_args) > 100 else tool_args
    print(f"\n🔧 Tool called -> {tool_name}({tool_args})")

    tool_name = tool_registry.get(tool_name)
    if tool_name is None:
        print(f"❌ Unknown tool: {tool_name}")

llm = ChatOpenAI(
    model = model_name)

# REPLACE WITH SqliteSaver !!!
memory = MemorySaver()

agent = create_agent(
    model = llm,
    tools = tools,
    system_prompt = SYSTEM_PROMPT,
    checkpointer = memory
)

config = {
        "configurable": {"thread_id": "my_session"},
        "recursion_limit": max_iterations
    }