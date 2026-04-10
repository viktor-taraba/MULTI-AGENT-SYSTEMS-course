from langchain.agents import create_agent
from config import (
    research_model_name, 
    SYSTEM_PROMPT_research,
    ToolCallLimit_research,
    port_search_mcp
)
from schemas import ResearchResult
from fastmcp import Client
from mcp_utils import mcp_tools_to_langchain
from supervisor import print_agent_step

from langchain.agents.middleware.tool_call_limit import ToolCallLimitMiddleware

tool_limiter = ToolCallLimitMiddleware(
    run_limit=ToolCallLimit_research, 
    exit_behavior="error"
)

port_search = f"http://127.0.0.1:{port_search_mcp}/mcp"

async def run_research(user_text: str) -> str:
    async with Client(port_search) as mcp_client:
        
        # Fetch and convert tools
        mcp_tools = await mcp_client.list_tools()
        lc_tools = mcp_tools_to_langchain(mcp_tools, mcp_client)

        # Create the agent with the dynamically fetched tools
        research_agent = create_agent(
            model=research_model_name,
            tools=lc_tools, 
            system_prompt=SYSTEM_PROMPT_research,
            response_format=ResearchResult,
            middleware=[tool_limiter]
        )

        # Run the agent while the connection is still open
        result = await research_agent.ainvoke({"messages": [("user", user_text)]})
             
        for msg in result["messages"][1:]:
            print_agent_step(msg, agent_name="Planner")

        return result["messages"][-1].content