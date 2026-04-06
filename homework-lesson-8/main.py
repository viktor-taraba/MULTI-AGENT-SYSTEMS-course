from langgraph.types import Command, Interrupt
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from supervisor import (
    plan,
    research,
    critique,
    print_agent_step
    )
import supervisor
from config import (
    SUPERVISOR_PROMPT, 
    supervisor_model_name, 
    max_iterations_supervisor
    )
from tools import save_report
import json
import uuid

def resume_graph(interrupt, decision_payload):
    """Resume the graph after an interrupt with the given decision."""
    resume_data = {interrupt.id: {"decisions": [decision_payload]}} if hasattr(interrupt, 'id') else {"decisions": [decision_payload]}
    return Command(resume=resume_data)

config = {
    "configurable": {"thread_id": "supervisor_thread"}, 
    "recursion_limit": max_iterations_supervisor}

def main():
    print("Research Agent")
    print("type 'exit' or 'quit' to quit")
    print("-" * 100)

    supervisor = create_agent(
                model=supervisor_model_name,
                tools=[plan, research, critique, save_report],
                system_prompt=SUPERVISOR_PROMPT,
                checkpointer=InMemorySaver(),
                middleware=[
                    HumanInTheLoopMiddleware(
                        interrupt_on={
                            "save_report": True,
                            "research_planner": False, 
                            "reseacrh_execution": False,
                            "research_critic": False
                        }),],)

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
            current_input = {"messages": [{"role": "user", "content": user_input}]}

            while True:
                interrupted = False

                for step in supervisor.stream(
                    current_input,
                    config=config
                ):
                    for update in step.values():

                        # HITL
                        if isinstance(update, tuple) and len(update) > 0 and isinstance(update[0], Interrupt):
                            interrupt = update[0]
                            interrupted = True
                
                            print(f"\n{'=' * 60}")
                            print(f" ⏸️  ACTION REQUIRES APPROVAL")
                            print(f"{'=' * 60}")
                
                            for request in interrupt.value.get("action_requests", []):
                                tool_name = request.get('name', request.get('action', 'N/A'))
                                print(f"   Tool:  {tool_name}")
                    
                                tool_args = request.get('args', {})
                                args_str = str(tool_args)
                                preview = args_str[:150] + "..." if len(args_str) > 150 else args_str
                                print(f"   Args:  {preview}")

                                if isinstance(tool_args, dict) and 'content' in tool_args:
                                    report_text = tool_args['content']
                                elif isinstance(tool_args, dict):
                                    # Fallback: Pretty print the JSON if it's a dict but has no 'content' key
                                    report_text = json.dumps(tool_args, indent=2, ensure_ascii=False)
                                else:
                                    report_text = str(tool_args)

                                # report preview and general information
                                lines = report_text.splitlines()
                                total_lines = len(lines)
                                total_symbols = len(report_text)
                                print(f"   Total lines in the report:  {total_lines}")
                                print(f"   Total symbols in the report:  {total_symbols}\n")
                                indented_content = "\n".join(f"   │ {line}" for line in lines[:25])
                                if len(lines) > 25:
                                    indented_content += f"\n│ ... (25/{len(lines)} rows) ..."
                                
                                formatted_name = "REPORT PREVIEW"
                                print(f"\n╭─── 📄 {formatted_name} {'─' * (40 - len(formatted_name))}")
                                print(indented_content)
                                print(f"╰{'─' * 46}\n")
                
                            # user input
                            choice = ""
                            while choice not in ["approve", "edit", "reject"]:
                                choice = input(" 👉 approve / edit / reject: ").strip().lower()

                            if choice == "approve":
                                print("\n ✅ Approved! Saving report...\n")
                                decision_payload = {"type": "approve"}
                                supervisor.current_research_session = str(uuid.uuid4()) # clearing research agent memory
                                supervisor.revision_counter = 0
                    
                            elif choice == "edit":
                                feedback = input(" ✏️  Your feedback: ").strip()
                                print("\n 🔄 Supervisor revises report based on feedback...\n")
                                decision_payload = {"type": "edit", "edited_action": {"feedback": feedback}}
                    
                            elif choice == "reject":
                                reason = input(" 🛑 Reason for rejection: ").strip() or "User rejected."
                                print("\n ❌ Rejected! Returning to Supervisor...\n")
                                decision_payload = {"type": "reject", "message": reason}

                            current_input = resume_graph(interrupt, decision_payload)
                            break
                
                        # usual agent messages
                        elif isinstance(update, dict):
                            for message in update.get("messages", []):
                                print_agent_step(message)
        
                    if interrupted:
                        break

                if not interrupted:
                    break

        except Exception as e:
            print(f"\n❌ An error occurred: {e}. Try again or type 'continue' (Don't worry, model remembers conversatio with you!")

if __name__ == "__main__":
    main()