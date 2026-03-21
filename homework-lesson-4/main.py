from agent import tool_execution, run_agent, create_database_if_not_exist, insert_session_database, insert_memory_database, truncate_database
from config import SYSTEM_PROMPT

def main():
    print("Research Agent")
    print("type 'exit' or 'quit' to quit")
    print("'delete history' to delete full conversation history (including previous conversations) and exit")
    print("-" * 40)

    create_database_if_not_exist();
    session_id = insert_session_database()

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            # тут зберігати самарі розмови (summary text and detail) + додати вивід по типу хвилинку, зберігаємо розмову
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit"):
            # тут зберігати самарі розмови (summary text and detail) + додати вивід по типу хвилинку, зберігаємо розмову
            print("Goodbye!")
            break

        if user_input.lower() in ("delete history"):
            print(truncate_database())
            break

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input},
        ]
        insert_memory_database(session_id, {"role": "user", "content": user_input}, 0)

        agent_response = run_agent(messages,session_id)
        if agent_response:
            print(agent_response)

        # to delete
        # print("")
        # print(messages)


if __name__ == "__main__":
    main()