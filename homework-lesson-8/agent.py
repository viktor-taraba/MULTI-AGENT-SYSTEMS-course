from openai import OpenAI
from tools import tool_registry, tools, write_report_tool_schema
from config import (
    FINAL_PROMPT, 
    max_iterations, 
    model_name, 
    max_steps_to_remember
)
import json
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

def tool_execution(item):
    tool_name = tool_registry.get(item.name)
    if tool_name is None:
        raise ValueError(f"Unknown tool: {item.name}")

    args = json.loads(item.arguments)
    args_str = str(args)
    args_str = args_str[:100] + "..." if len(args_str) > 100 else args_str
    print(f"🔧 Tool called -> {item.name}({args_str})")

    result = tool_name(**args)
            
    content_str = str(result)
    content_str = content_str[:100] + "..." if len(content_str) > 100 else content_str
    print(f"✅ Result ({item.name}): {content_str}")

    return {
        "type": "function_call_output",
        "call_id": item.call_id,
        "output": json.dumps(result)
    }

def last_call(final_prompt_text, messages, session_id):
    print(f"\n⚠️ Agent stopped: Reached the maximum limit of iterations. Generating final report from gathered data...")
    tools = [write_report_tool_schema]

    messages.append({
        "role": "user",
        "content": final_prompt_text
    })
    
    response = client.responses.create(
            model = model_name,
            input = messages,
            tools = tools)

    messages_in_output = [item for item in response.output if item.type == "message"]

    if messages_in_output:
        final_text = messages_in_output[0].content[0].text
        print(f"\n🤖 Agent:\n{final_text}")
        insert_memory_database(session_id, {"role": "assistant", "content": final_text}, response)

    messages.extend(response.output)

    for item in response.output:
        if item.type == "function_call":
            insert_memory_database(session_id, {"role": "assistant", "content": f"Tool called: {item.name}({item.arguments})"}, response)

            if item.name == "write_report":
                tool_result_msg = tool_execution(item)
                messages.append(tool_result_msg)
                insert_memory_database(session_id, {"role": "tool", "content": tool_result_msg["output"]}, None)
                return f"\n✅ Finished: report generated. You can continue dialog with our agent: this conversation is not forgotten!"

            else:
                return f"\n🤖 Oh no... Something is not right. Please try again. Do not worry: this conversation is not forgotten, try to continue it"
    return ""

def run_agent(messages, session_id):
    for iteration in range(1, max_iterations + 1):
        print(f"\n🔄 Iteration {iteration} - Thinking...")

        response = client.responses.create(
            model = model_name,
            input = messages,
            tools = tools)

        messages_in_output = [item for item in response.output if item.type == "message"]
        if messages_in_output:
            final_text = messages_in_output[0].content[0].text
            insert_memory_database(session_id, {"role": "assistant", "content": final_text}, response)
            return f"\n🤖 Agent:\n{final_text}"

        # If no final message, append the model's tool calls to the history
        messages.extend(response.output)
        # Execute the tool calls
        for item in response.output:
            if item.type == "function_call":
                insert_memory_database(session_id, {"role": "assistant", "content": f"Tool called: {item.name}({item.arguments})"}, response)
                tool_result_msg = tool_execution(item)
                messages.append(tool_result_msg)
                insert_memory_database(session_id, {"role": "tool", "content": tool_result_msg["output"]}, None)
 
        messages = truncate_history_safely(messages)

        if iteration == max_iterations:
            last_call(FINAL_PROMPT, messages, session_id)
            break

def get_msg_type(msg):
    """Safely extracts the message type whether it's a dict or an object."""
    if isinstance(msg, dict):
        return msg.get("type", "")
    return getattr(msg, "type", "")