from tools import web_search, read_url
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
from config import SYSTEM_PROMPT, max_iterations, model_name, model_temerature
from dotenv import load_dotenv
load_dotenv()
import warnings

warnings.filterwarnings(
    "ignore", 
    message=".*Core Pydantic V1 functionality isn't compatible with Python 3.14.*", 
    category=UserWarning
)

llm = ChatOpenAI(
    model = model_name, 
    temperature = model_temerature)

tools = [web_search, read_url]

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
    
user_query = "what is budget centralization?" #"ЮГОВ-проект - що це?"
print(f"👤 Користувач: {user_query}\n")
print("-" * 40)
    
try:
    for event in agent.stream({"messages": [("user", user_query)]}, config=config):
        for node_name, node_data in event.items():
            if "messages" in node_data:
                latest_message = node_data["messages"][-1]
                latest_message.pretty_print()
                    
except Exception as e:
    if "Recursion limit" in str(e):
        print(f"\n⚠️ Agent stopped: Reached the maximum limit of {max_iterations} iterations.")
    else:
        print(f"\n❌ An error occurred: {e}")

'''
followup_input = messages.copy()

# Set a maximum number of iterations to prevent infinite loops
max_iterations = 50
iteration = 0
while iteration < max_iterations:
    iteration += 1

    response = client.responses.create(
        model="gpt-5-mini",
        input=followup_input,
        tools=tools,
    )

    # 2. Check if the model returned a final message
    messages_in_output = [item for item in response.output if item.type == "message"]
    if messages_in_output:
        final_text = messages_in_output[0].content[0].text
        print(f"\n💬 Final response:\n{final_text}")
        break

    # 3. If no final message, append the model's tool calls to the history
    followup_input.extend(response.output)

    # 4. Execute the tool calls
    for item in response.output:
        if item.type == "function_call":
            func = tool_registry.get(item.name)
            if func is None:
                raise ValueError(f"Unknown tool: {item.name}")

            args = json.loads(item.arguments)
            print(f"🔧 Calling: {item.name}({args})")

            # Execute the function
            result = func(**args)
            # to delete
            # print("Function Calling result:", json.dumps(result, indent=2))

            # Append the result back to the conversation history
            followup_input.append({
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": json.dumps(result),
            })
else:
    print("\n⚠️ Agent reached the maximum number of iterations without providing a final answer.")
'''