from langchain.agents import create_agent
from schemas import CritiqueResult
from config import (
    critic_model_name, 
    SYSTEM_PROMPT_critic,
    ToolCallLimit_critic,
    port_search_mcp
)
from fastmcp import Client
from mcp_utils import mcp_tools_to_langchain
from supervisor import print_agent_step
from langchain.agents.middleware.tool_call_limit import ToolCallLimitMiddleware

tool_limiter = ToolCallLimitMiddleware(
    run_limit=ToolCallLimit_critic, 
    exit_behavior="error"
)

port_search = f"http://127.0.0.1:{port_search_mcp}/mcp"

async def run_critic(user_text: str) -> str:
    async with Client(port_search) as mcp_client:
        
        mcp_tools = await mcp_client.list_tools()
        lc_tools = mcp_tools_to_langchain(mcp_tools, mcp_client)

        critic_agent = create_agent(
            model=critic_model_name,
            tools=lc_tools, 
            system_prompt=SYSTEM_PROMPT_critic,
            response_format=CritiqueResult,
            middleware=[tool_limiter]
        )

        final_response = ""
        # Use .astream() to stream graph updates in real-time
        async for step in critic_agent.astream({"messages": [("user", user_text)]}):
            
            for node_name, update in step.items():
                if isinstance(update, dict) and "messages" in update:
                    
                    messages = update["messages"]
                    if not isinstance(messages, list):
                        messages = [messages]
                        
                    for msg in messages:
                        print_agent_step(msg, agent_name="Critic")
                        # Capture the latest AI message content so we can return it at the end
                        if getattr(msg, "type", None) == "ai" and getattr(msg, "content", ""):
                            final_response = msg.content
        return final_response