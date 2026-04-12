from langchain.agents import create_agent
from schemas import ResearchPlan
from config import (
    planner_model_name, 
    SYSTEM_PROMPT_planner,
    ToolCallLimit_planner,
    port_search_mcp,
    FINAL_PROMPT_planner
)
from fastmcp import Client
from mcp_utils import mcp_tools_to_langchain
from supervisor import print_agent_step
from langchain.agents.middleware.tool_call_limit import ToolCallLimitMiddleware
from langchain_core.messages import ToolMessage

tool_limiter = ToolCallLimitMiddleware(
    run_limit=ToolCallLimit_planner, 
    exit_behavior="error"
)

port_search = f"http://127.0.0.1:{port_search_mcp}/mcp"

async def run_planner(user_text: str) -> str:
    async with Client(port_search) as mcp_client:

        # Fetch and convert tools
        mcp_tools = await mcp_client.list_tools()
        lc_tools = mcp_tools_to_langchain(mcp_tools, mcp_client)

        planner_agent = create_agent(
            model=planner_model_name,
            tools=lc_tools, 
            system_prompt=SYSTEM_PROMPT_planner,
            response_format=ResearchPlan,
            middleware=[tool_limiter]
        )

        final_response = ""
        messages_history = [("user", user_text)]
        
        try:
            # Use .astream() to stream graph updates in real-time
            async for step in planner_agent.astream({"messages": messages_history}):
                for node_name, update in step.items():
                    if isinstance(update, dict) and "messages" in update:
                        messages = update["messages"]
                        if not isinstance(messages, list):
                            messages = [messages]
                            
                        for msg in messages:
                            messages_history.append(msg)
                            print_agent_step(msg, agent_name="Planner")
                            if getattr(msg, "type", None) == "ai" and getattr(msg, "content", ""):
                                final_response = msg.content
                                
        except Exception as e:
            if type(e).__name__ == "ToolCallLimitExceededError":
                print_agent_step(f"\n⚠️ Researcher reached tool call limit. Forcing final output...",agent_name="Planner")
                
                # Check if the last message was an AI asking for tools
                last_msg = messages_history[-1] if messages_history else None
                if getattr(last_msg, "type", None) == "ai" and getattr(last_msg, "tool_calls", None):
                    # OpenAI's API requirement by closing open tool calls
                    for tc in last_msg.tool_calls:
                        messages_history.append(
                            ToolMessage(
                                tool_call_id=tc["id"],
                                name=tc["name"],
                                content="System Abort: Tool execution cancelled because iteration limit was reached."
                            )
                        )
                
                messages_history.append(("user", FINAL_PROMPT_planner))
                fallback_agent = create_agent(
                    model=planner_model_name,
                    tools=[], 
                    system_prompt=FINAL_PROMPT_planner,
                    response_format=ResearchPlan,
                    middleware=[] 
                )
                fallback_result = await fallback_agent.ainvoke({"messages": messages_history})
                
                if "messages" in fallback_result:
                    for msg in fallback_result["messages"]:
                        if getattr(msg, "type", None) == "ai" and getattr(msg, "content", ""):
                            print_agent_step(msg, agent_name="Planner")
                            final_response = msg.content
            else:
                raise e
                
        return final_response