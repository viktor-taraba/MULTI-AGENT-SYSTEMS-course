from agent import ( 
    run_agent, 
    create_database_if_not_exist, 
    insert_session_database, 
    insert_memory_database, 
    truncate_database, 
    summarize_memory_database,
    ensure_previous_session_summarized,
    get_memory_database_summary
)
from config import SYSTEM_PROMPT, model_name_for_summary

def main():
    print("Research Agent")
    print("type 'exit' or 'quit' to quit")
    print("-" * 100)

    dynamic_system_prompt = SYSTEM_PROMPT
    messages = [
        {"role": "system", "content": dynamic_system_prompt}
    ]

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSaving summary pf our conversation...")
            summarize_memory_database(model_name_for_summary, session_id)
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit"):
            print("\nSaving summary pf our conversation...")
            summarize_memory_database(model_name_for_summary, session_id)
            print("Goodbye!")
            break

        messages.append({"role": "user", "content": user_input})

        agent_response = run_agent(messages,session_id)
        if agent_response:
            print(agent_response)

if __name__ == "__main__":
    main()