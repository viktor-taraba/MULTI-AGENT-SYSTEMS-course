from openai import OpenAI
from tools import tool_registry, tools
from config import SYSTEM_PROMPT, max_iterations, model_name, model_temerature
import json
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": "ЮГОВ-проект - що це?"},
]

response = client.responses.create(
    model="gpt-5-mini",
    input=messages,
    tools=tools,
)

followup_input = messages.copy()

# memory

# Set a maximum number of iterations to prevent infinite loops
iteration = 0
while iteration < max_iterations:
    iteration += 1

    response = client.responses.create(
        model="gpt-5-mini",
        input=followup_input,
        tools=tools,
    )

    # Check if the model returned a final message
    messages_in_output = [item for item in response.output if item.type == "message"]
    if messages_in_output:
        final_text = messages_in_output[0].content[0].text
        print(f"\n💬 Final response:\n{final_text}")
        break

    # If no final message, append the model's tool calls to the history
    followup_input.extend(response.output)

    # Execute the tool calls
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