from langchain.agents import create_agent
from schemas import CritiqueResult
from config import (
    critic_model_name, 
    SYSTEM_PROMPT_critic,
    port_search_mcp
)
from schemas import ResearchResult
from fastmcp import Client
from mcp_utils import mcp_tools_to_langchain
from supervisor import print_agent_step

port_search = f"http://127.0.0.1:{port_search_mcp}/mcp"

async def run_critic(user_text: str) -> str:
    async with Client(port_search) as mcp_client:
        
        mcp_tools = await mcp_client.list_tools()
        lc_tools = mcp_tools_to_langchain(mcp_tools, mcp_client)

        critic_agent = create_agent(
            model=critic_model_name,
            tools=lc_tools, 
            system_prompt=SYSTEM_PROMPT_critic,
            response_format=CritiqueResult
        )

        result = await critic_agent.ainvoke({"messages": [("user", user_text)]})

        for msg in result["messages"][1:]:
            print_agent_step(msg, agent_name="Planner")
        return result["messages"][-1].content