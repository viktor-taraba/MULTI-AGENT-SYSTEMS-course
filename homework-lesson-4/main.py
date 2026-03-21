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
    print("'delete history' to delete full conversation history (including previous conversations) and exit")
    print("-" * 100)

    create_database_if_not_exist();
    session_id = insert_session_database()
    ensure_previous_session_summarized(session_id)

    past_summaries = get_memory_database_summary(session_id)

    dynamic_system_prompt = SYSTEM_PROMPT
    if past_summaries:
        dynamic_system_prompt += "\n\n--- MEMORY OF PAST CONVERSATIONS ---\n"
        for i, summary in enumerate(past_summaries, 1):
            dynamic_system_prompt += f"Session {i}: {summary}\n"

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

        if user_input.lower() in ("delete history"):
            print(truncate_database())
            break

        insert_memory_database(session_id, {"role": "user", "content": user_input}, 0)
        messages.append({"role": "user", "content": user_input})

        if len(messages) > 51:
            system_message = messages[0]
            recent_messages = messages[-50:]
    
            while recent_messages and (
                isinstance(recent_messages[0], dict) and 
                recent_messages[0].get("type") == "function_call_output"
            ):
                recent_messages.pop(0)
        
            messages = [system_message] + recent_messages

        agent_response = run_agent(messages,session_id)
        if agent_response:
            print(agent_response)

if __name__ == "__main__":
    main()