from acp_sdk.models import Message, MessagePart
from acp_sdk.server import Server
from acp_sdk.models import Message, MessagePart
from agents.planner import run_planner
from agents.critic import run_critic
from agents.research import run_research
from config import port_acp_server
from dotenv import load_dotenv
load_dotenv()

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
    output_content = await run_research(user_text)
    return Message(role="agent", parts=[MessagePart(content=output_content)])

@acp_server.agent(name="critic", description="Evaluates the resulting work to identify errors and ensure high-quality output.")
async def critic_handler(input: list[Message]) -> Message:
    user_text = input[-1].parts[0].content
    output_content = await run_critic(user_text)
    return Message(role="agent", parts=[MessagePart(content=output_content)])

def run_acp():
    acp_server.run(port=port_acp_server)

if __name__ == "__main__":
    print(f"✅ Starting ACP Server on {acp_adress}")
    try:
        acp_server.run(host="127.0.0.1", port=port_acp_server)
    except KeyboardInterrupt:
        print(f"🛑 ACP Server {acp_adress} stopped")