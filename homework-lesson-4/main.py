from agent import tool_execution, run_agent
from config import SYSTEM_PROMPT

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

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input},
        ]

        agent_response = run_agent(messages)
        if agent_response:
            print(agent_response)

        # to delete
        print("")
        print(messages)


if __name__ == "__main__":
    main()