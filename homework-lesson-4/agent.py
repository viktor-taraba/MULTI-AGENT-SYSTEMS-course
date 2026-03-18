from openai import OpenAI
from tools import tool_registry, tools
from config import SYSTEM_PROMPT, max_iterations, model_name
import json
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": "Нещодавні новини про Україну"},
]

followup_input = messages.copy()

# memory

# Set a maximum number of iterations to prevent infinite loops
iteration = 0
while iteration < max_iterations:
    iteration += 1
    # додати debug mode - виводити повний текст усіх запусків, ітерації, т. д.
    print(f"\n🔄 Iteration {iteration} - Sending input to the model...")

    # тут переписати на ф-ї, і в main.py юзати їх + чекнути структуру і розбивку на agent та main

    response = client.responses.create(
        model = model_name,
        input = followup_input,
        tools = tools
    )

    # Check if the model returned a final message
    messages_in_output = [item for item in response.output if item.type == "message"]
    if messages_in_output:
        final_text = messages_in_output[0].content[0].text
        print(f"\n🤖 Agent:\n{final_text}")
        break

    # If no final message, append the model's tool calls to the history
    followup_input.extend(response.output)

    # Execute the tool calls
    for item in response.output:
        if item.type == "function_call":
            tool_name = tool_registry.get(item.name)
            if tool_name is None:
                raise ValueError(f"Unknown tool: {item.name}")

            args = json.loads(item.arguments)
            args_str = str(args)
            args_str = args_str[:150] + "..." if len(args_str) > 150 else args_str
            print(f"🔧 Tool called -> {tool_name}({args_str})")

            result = tool_name(**args)
            
            content_str = str(result)
            content_str = content_str[:150] + "..." if len(content_str) > 150 else content_str
            print(f"✅ Result ({tool_name}): {content_str}")

            # Append the result back to the conversation history
            followup_input.append({
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": json.dumps(result),
            })

            # ідея для пам'яті - зберігати такий же результат в БД, можливо з додатковою інфою
            # перед тим як знову давати користувачу можлмивість введення, зберегти в БД в окремій таблиці самарі розмови з таким-то ід
            # і потім при наступному виклику передавати агенту самарі цієї розмови з таблиці як контекст для наступних відповідей
else:
    print("\n⚠️ Agent reached the maximum number of iterations without providing a final answer.")