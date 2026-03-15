# llm = ...

# tools = ...

# memory = ...

# agent = ...

from tools import web_search, read_url, web_search_tool_schema, read_url_tool_schema
from openai import OpenAI
import json
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

# Tool registry — maps tool names to Python functions
tool_registry = {"web_search": web_search, "read_url": read_url}

# Step 1: Define tools and call the API
tools = [web_search_tool_schema, read_url_tool_schema]
tools

messages = [
    {"role": "system", "content": "You are a Senior Analyst with 10 years of experience.\
      Your task is to receive a question from the user, search and structure information using a appropriate tools, gathers findings, and generate a structured highly detailed, comprehensive Markdown report.\
      CRITICAL RULES:\
      1. DO NOT rely solely on search engine snippets. They are too brief.\
      2. After using 'web_search', you MUST use the 'read_url' tool on at least 1-2 of the most relevant links to gather deep context, statistics, and specific details.\
      3. Only generate your final report AFTER you have read the full text of the relevant sources."},
     {"role": "user", "content": "ЮГОВ-проект - що це?"},#"Нещодавні новини про Україну (з коротким підсумком)"},#"LangChain vs LlamaIndex RAG"},
]

response = client.responses.create(
    model="gpt-5-mini",
    input=messages,
    tools=tools,
)

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