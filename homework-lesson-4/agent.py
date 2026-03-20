from openai import OpenAI
from tools import tool_registry, tools, write_report_tool_schema
from config import FINAL_PROMPT, max_iterations, model_name
import json
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

# memory
    # ідея для пам'яті - зберігати такий же результат в БД, можливо з додатковою інфою
    # перед тим як знову давати користувачу можлмивість введення, зберегти в БД в окремій таблиці самарі розмови з таким-то ід
    # і потім при наступному виклику передавати агенту самарі цієї розмови з таблиці як контекст для наступних відповідей

def create_or_use_database():
    pass

def get_memory_database():
    pass

def insert_memory_database():
    pass

def summarize_memory_database():
    pass

def tool_execution(item):
    tool_name = tool_registry.get(item.name)
    if tool_name is None:
        raise ValueError(f"Unknown tool: {item.name}")

    args = json.loads(item.arguments)
    args_str = str(args)
    args_str = args_str[:150] + "..." if len(args_str) > 150 else args_str
    print(f"🔧 Tool called -> {item.name}({args_str})")

    result = tool_name(**args)
            
    content_str = str(result)
    content_str = content_str[:150] + "..." if len(content_str) > 150 else content_str
    print(f"✅ Result ({item.name}): {content_str}")

    return {
        "type": "function_call_output",
        "call_id": item.call_id,
        "output": json.dumps(result)
    }

def last_call(final_prompt_text, messages):
    print(f"\n⚠️ Agent stopped: Reached the maximum limit of iterations. Generating final report from gathered data...")
    tools = [write_report_tool_schema]

    messages.append({
        "role": "user",
        "content": FINAL_PROMPT
    })
    
    response = client.responses.create(
            model = model_name,
            input = messages,
            tools = tools)
    
    messages_in_output = [item for item in response.output if item.type == "message"]
    if messages_in_output:
        final_text = messages_in_output[0].content[0].text
        print(f"\n🤖 Agent:\n{final_text}")

    messages.extend(response.output)
    for item in response.output:
        if item.type == "function_call":
            if item.name == "write_report":
                tool_result_msg = tool_execution(item)
                messages.append(tool_result_msg)
                return f"\n✅ Finished: report generated. You can continue dialog with our agent: this conversation is not forgotten!"
            else:
                return f"\n🤖 Oh no... Something is not right. Please try again. Do not worry: this conversation is not forgotten, try to continue it"
    return ""


def run_agent(messages): # debug: bool = True # додати debug mode - виводити повний текст усіх запусків, ітерації, т. д.
    for iteration in range(1, max_iterations + 1):
        print(f"\n🔄 Iteration {iteration} - Sending input to the model...")

        response = client.responses.create(
            model = model_name,
            input = messages,
            tools = tools)

        messages_in_output = [item for item in response.output if item.type == "message"]
        if messages_in_output:
            final_text = messages_in_output[0].content[0].text
            return f"\n🤖 Agent:\n{final_text}"

        # If no final message, append the model's tool calls to the history
        messages.extend(response.output)
        # Execute the tool calls
        for item in response.output:
            if item.type == "function_call":
                tool_result_msg = tool_execution(item)
                messages.append(tool_result_msg)

        if iteration == max_iterations:
            last_call(FINAL_PROMPT, messages)
            break