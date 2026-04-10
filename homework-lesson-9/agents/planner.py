from langchain.agents import create_agent
from schemas import ResearchPlan
from config import (
    planner_model_name, 
    SYSTEM_PROMPT_planner,
    port_search_mcp
)
from fastmcp import Client
from mcp_utils import mcp_tools_to_langchain
from supervisor import print_agent_step

port_search = f"http://127.0.0.1:{port_search_mcp}/mcp"

async def run_planner(user_text: str) -> str:
    # Connect to your SearchMCP server (Change port if needed)
    async with Client(port_search) as mcp_client:
        
        # 1. Fetch and convert tools
        mcp_tools = await mcp_client.list_tools()
        lc_tools = mcp_tools_to_langchain(mcp_tools, mcp_client)

        # 2. Create the agent with the dynamically fetched tools
        planner_agent = create_agent(
            model=planner_model_name,
            tools=lc_tools, 
            system_prompt=SYSTEM_PROMPT_planner,
            response_format=ResearchPlan
        )

        # 3. Run the agent while the connection is still open!
        result = await planner_agent.ainvoke({"messages": [("user", user_text)]})
             
        # 4. Iterate through the message history to print the steps!
        # (We use [1:] to skip the first message, which is just the user's input)
        for msg in result["messages"][1:]:
            print_agent_step(msg, agent_name="Planner")

        # 5. Return the final string to the ACP server
        return result["messages"][-1].content