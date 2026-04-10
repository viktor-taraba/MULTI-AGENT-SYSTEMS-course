from acp_sdk.models import Message, MessagePart
from acp_sdk.server import Server
from acp_sdk.client import Client as ACPClient
from acp_sdk.models import Message, MessagePart
from agents.planner import run_planner
from agents.critic import critic_agent
from agents.research import research_agent
from config import port_acp_server
import asyncio
import threading
import time
"""
├── acp_server.py        # ACP server with 3 agents (planner, researcher, critic)
├── agents/
│   ├── __init__.py
│   ├── planner.py       # Planner Agent definition (prompt + response_format)
│   ├── research.py      # Research Agent definition
│   └── critic.py        # Critic Agent definition
"""
"""
 2. ACP Server (агенти)
Створіть один ACP сервер (порт 8903) з трьома агентами. Кожен агент:

Підключається до SearchMCP через fastmcp.Client
Конвертує MCP tools у LangChain format (mcp_tools_to_langchain з лекції 9)
Створений через create_agent з system prompt з homework-8
Повертає Message(role="agent", ...)
Planner і Critic використовують response_format для структурованого виводу (як у homework-8).

 1 ACP сервер з 3 агентами (planner, researcher, critic)
 Кожен ACP агент підключається до SearchMCP через fastmcp.Client
 Кожен ACP агент створений через create_agent
 Supervisor оркеструє агентів через acp_sdk.client.Client
 
 """

acp_adress = f"http://127.0.0.1:{port_acp_server}"

acp_server = Server()

print("✅ ACP Server created (acp-sdk)")

@acp_server.agent(name="planner", description="Breaks complex goals into a structured sequence of steps.")
async def planner_handler(input: list[Message]) -> Message:
    user_text = input[-1].parts[0].content
    output_content = await run_planner(user_text)
    return Message(role="agent", parts=[MessagePart(content=output_content)])

@acp_server.agent(name="researcher", description="Gathers the factual information and writes report.")
async def researcher_handler(input: list[Message]) -> Message:
    user_text = input[-1].parts[0].content
    result = await research_agent.ainvoke({"messages": [("user", user_text)]})
    return Message(role="agent", parts=[MessagePart(content=result["messages"][-1].content)])

@acp_server.agent(name="critic", description="Evaluates the resulting work to identify errors and ensure high-quality output.")
async def critic_handler(input: list[Message]) -> Message:
    user_text = input[-1].parts[0].content
    result = await critic_agent.ainvoke({"messages": [("user", user_text)]})
    return Message(role="agent", parts=[MessagePart(content=result["messages"][-1].content)])

def run_acp():
    acp_server.run(port=port_acp_server)

async def demo_acp():
    async with ACPClient(base_url=acp_adress, headers={"Content-Type": "application/json"}) as client:
        # Discovery
        agents = [a async for a in client.agents()]
        print("ACP Discovery:")
        for a in agents:
            print(f"   {a.name}: {a.description}")
        print()

        # Call planner
        print('-' * 50)
        print("Calling 'planner'...")
        run = await client.run_sync(
            agent="planner",
            input=[Message(role="user", parts=[MessagePart(content="What is BM25 algorithm and how is it used in search engines?")])],
        )
        output = run.output[-1].parts[0].content
        print(f"**Result:**\n{output}")
        print()
        print('-' * 50)
        print()

        """
        # Call researcher
        print('-' * 50)
        print("Calling 'researcher'...")
        run = await client.run_sync(
            agent="researcher",
            input=[Message(role="user", parts=[MessagePart(content="What is BM25 algorithm and how is it used in search engines?")])],
        )
        output = run.output[-1].parts[0].content
        print(f"**Result:**\n{output}")
        print()
        print('-' * 50)
        """

if __name__ == "__main__":
    threading.Thread(target=run_acp, daemon=True).start()
    time.sleep(2)
    print(f"✅ ACP Server running at http://127.0.0.1:{acp_adress}")
    asyncio.run(demo_acp())