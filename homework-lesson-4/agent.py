from openai import OpenAI
from tools import tool_registry, tools, write_report_tool_schema
from config import FINAL_PROMPT, max_iterations, model_name, memory_database_name
import json
import sqlite3
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

# memory
    # ідея для пам'яті - зберігати такий же результат в БД, можливо з додатковою інфою
    # перед тим як знову давати користувачу можлмивість введення, зберегти в БД в окремій таблиці самарі розмови з таким-то ід
    # і потім при наступному виклику передавати агенту самарі цієї розмови з таблиці як контекст для наступних відповідей

def create_database_if_not_exist():
    conn = sqlite3.connect(memory_database_name)
    conn.execute("pragma foreign_keys = 1;")
    cursor = conn.cursor()
    cursor.execute('''
        create table if not exists tb_sessions(
            session_id      integer primary key autoincrement,
            model_name      text not null,
            summary_header  text null,
            summary_text    text null,
            created_at      datetime default current_timestamp
        );
    ''')
    conn.commit()
    cursor.execute('''
        create table if not exists tb_agent_history (
            id              integer primary key autoincrement,
            session_id      integer not null,
            role            text not null,
            content         text,
            raw_json        text,
            prompt_tokens   integer,
            result_tokens   integer,
            total_tokens    integer,
            created_at      datetime default current_timestamp,
            foreign key (session_id) references tb_sessions (session_id) on delete cascade
        );
    ''')
    conn.commit()
    conn.close()

def insert_session_database():
    conn = sqlite3.connect(memory_database_name)
    cursor = conn.cursor()
    cursor.execute(
        "insert into tb_sessions (model_name) VALUES (?)",
        (model_name,)
    )
    conn.commit()
    new_session_id = cursor.lastrowid 
    conn.close()

    return new_session_id

def insert_memory_database(session_id, session_message, response_obj):
    """
    Inserts a single message or tool call into the tb_agent_history table.
    
    Args:
        session_id (int): The ID returned from insert_session_database().
        session_message (dict): The message dictionary (e.g., {"role": "user", "content": "..."}).
        response_obj: The raw response object from OpenAI (used to extract tokens).
    """
    conn = sqlite3.connect(memory_database_name)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()
    
    role = session_message.get("role", "unknown")
    content = session_message.get("content")
    
    prompt_tokens, result_tokens, total_tokens, raw_json = 0, 0, 0, ""
    
    if response_obj and hasattr(response_obj, "usage") and response_obj.usage:
        prompt_tokens = response_obj.usage.input_tokens
        result_tokens = response_obj.usage.output_tokens
        total_tokens = response_obj.usage.total_tokens
        raw_json = response_obj.model_dump_json()
        
    cursor.execute('''
        insert into tb_agent_history 
        (session_id, role, content, raw_json, prompt_tokens, result_tokens, total_tokens)
        values (?, ?, ?, ?, ?, ?, ?)
    ''', (session_id, role, content, raw_json, prompt_tokens, result_tokens, total_tokens))
    conn.commit()
    conn.close()

def truncate_database():
    conn = sqlite3.connect(memory_database_name)
    conn.execute("pragma foreign_keys = 1;")
    cursor = conn.cursor()
    cursor.execute("delete from tb_sessions")
    conn.commit()
    conn.close()
    return "✅ Database truncated: all conversation history has been deleted."

def get_memory_database():
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

def last_call(final_prompt_text, messages, session_id):
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
        insert_memory_database(session_id, {"role": "assistant", "content": final_text}, response)

    messages.extend(response.output)

    for item in response.output:
        if item.type == "function_call":
            insert_memory_database(session_id, {"role": "assistant", "content": f"Tool called: {item.name}"}, response)

            if item.name == "write_report":
                tool_result_msg = tool_execution(item)
                messages.append(tool_result_msg)
                insert_memory_database(session_id, {"role": "tool", "content": tool_result_msg["output"]}, None)
                return f"\n✅ Finished: report generated. You can continue dialog with our agent: this conversation is not forgotten!"

            else:
                return f"\n🤖 Oh no... Something is not right. Please try again. Do not worry: this conversation is not forgotten, try to continue it"
    return ""

def run_agent(messages, session_id): # debug: bool = True # додати debug mode - виводити повний текст усіх запусків, ітерації, т. д.
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

        if iteration == max_iterations:
            last_call(FINAL_PROMPT, messages, session_id)
            break