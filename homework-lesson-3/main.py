from agent import agent, config
import warnings

warnings.filterwarnings(
    "ignore", 
    message=".*Core Pydantic V1 functionality isn't compatible with Python 3.14.*", 
    category=UserWarning
)

def main():
    print("Research Agent (type 'exit' to quit)")
    print("-" * 40)

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break
        
        try:
            for chunk in agent.stream(
                {"messages": [("user", user_input)]},config=config
            ):
                if "model" in chunk and "messages" in chunk["model"]:
                    for msg in chunk["model"]["messages"]:
                        
                        if hasattr(msg, "content") and msg.content:
                            print("")
                            print(f"\n🤖 Agent:\n{msg.content}")

                        # Extract information about the tool being called and its parameters
                        if hasattr(msg, "tool_calls") and msg.tool_calls:
                            for tool_call in msg.tool_calls:
                                tool_name = tool_call.get("name")
                                tool_args = str(tool_call.get("args"))
                                tool_args = tool_args[:150] + "..." if len(tool_args) > 150 else tool_args
                                print("")
                                print(f"🔧 Tool called -> {tool_name}({tool_args})")

                # 2. Tools Node: The tool has finished running and returned data
                elif "tools" in chunk and "messages" in chunk["tools"]:
                    for msg in chunk["tools"]["messages"]:
                        tool_name = msg.name
                        content_str = str(msg.content)
                        preview = content_str[:150] + "..." if len(content_str) > 150 else content_str
                        
                        print(f"✅ Result ({tool_name}): {preview}")
                        
        except Exception as e:
            if "Recursion limit" in str(e):
                print(f"\n⚠️ Agent stopped: Reached the maximum limit of iterations. Try again or type 'continue' (Don't worry, model remembers conversatio with you!)")
            else:
                print(f"\n❌ An error occurred: {e}. Try again or type 'continue' (Don't worry, model remembers conversatio with you!")


if __name__ == "__main__":
    main()