from langchain.agents import create_agent
from langchain_core.tools import tool
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.types import Command, Interrupt
from typing import Literal
from agents.planner import planner
from agents.coder import coder
from agents.reviewer import reviewer
from dotenv import load_dotenv
from langfuse import get_client
from langfuse.langchain import CallbackHandler
from datetime import datetime
from config import (
    tool_preview_len
    )
from tools import tool_registry
import uuid
load_dotenv()

"""
2.1. Приклад: AI Team — Planner–Coder–Reviewer
Класична "AI-команда" для software development:

User Request → Planner → Coder → Reviewer → (loop if needed) → Final Output
Planner: Отримує задачу, розбиває на конкретні кроки реалізації
Coder: Пише код за планом, використовує інструменти (file write, shell exec)
Reviewer: Перевіряє код на помилки, стиль, відповідність плану. Якщо є проблеми — повертає Coder-у
Важливі design decisions:

Чи бачить Reviewer весь контекст (план + код), чи тільки код?
Скільки ітерацій допускається перед ескалацією до людини?
Як передається контекст між агентами — повністю або compact summary?

Does it make sense to use cheaper model to filter user question as a first step in a multi-agent system if it is not relevant to the covered tasks?

Yes, it makes complete sense. In fact, this is an industry-standard architectural pattern often referred to as Semantic Routing or Gating.

Using a smaller, faster model as the "front door" to your heavier, more expensive multi-agent system provides several distinct advantages, but it does come with a few trade-offs you will need to manage.

Workflow (LangGraph)
1) START → BA: користувач надсилає user story.
2) BA досліджує контекст (DuckDuckGo + RAG), формує SpecOutput.
3) HITL gate: користувач затверджує специфікацію або повертає з feedback → BA переробляє (цикл до затвердження). Запобігає розробці за неправильними вимогами.
4) BA → Developer: передача затвердженої SpecOutput.
5) Developer пише код (Python REPL + file write), повертає CodeOutput. ⚠️ LLM-згенерований код потрібно запускати з обмеженнями: timeout, заборонені модулі (os, subprocess, shutil), обмеження на розмір output.
6) Developer → QA: передача CodeOutput.
7) QA оцінює код, повертає ReviewOutput (with_structured_output).
8) Conditional edge (Command API): verdict=REVISION_NEEDED і iteration < 5 → Developer з payload (issues + suggestions). Інакше → END.
"""

# add HITL
# check: reducer = add
# переробити RAG (щоб для таблиць повертав повний файл, а не лише фрагмент)
# подивитися як отримати фактичний план запиту, а не лише оціночний
# для оціночного плану запиту покращити форматування аутпуту
# подумати над додатковими ідеями для тулів (можливо для створення окремих .sql файлів з кодом)
# додати як в дз пам'ять (щоб пам'ятав попередні діалоги в межах сесії)
# додати тести по тулах (для кожного агента окремо) (все через deepeval)
# Conditional edge (Command API): verdict=REVISION_NEEDED і iteration < 5 → Developer з payload (issues + suggestions). Інакше → END.
# додати обмеження на timeout при запуску коду через тул execution
# винести граф в окремий файл в проекті, щоб main був більш читабельний

langfuse = get_client()
langfuse_handler = CallbackHandler()

session_id = f"{datetime.now().isoformat()}-course-project-{uuid.uuid4().hex[:8]}"
user_id="viktor_hw_12"
tags=["course-project", "multi-agent"]

# Reviewer routing: return string, not Command (conditional edges require strings)
def review_router(state: MessagesState) -> Literal["coder", "__end__"]:
    """Route based on reviewer verdict."""
    last_msg = state["messages"][-1].content
    if "APPROVED" in last_msg.upper():
        return END
    return "coder"

# Build the graph: planner → coder → reviewer → (loop or end)
graph = StateGraph(MessagesState)
graph.add_node("planner", planner)
graph.add_node("coder", coder)
graph.add_node("reviewer", reviewer)
graph.add_edge(START, "planner")
graph.add_edge("planner", "coder")
graph.add_edge("coder", "reviewer")
graph.add_conditional_edges("reviewer", review_router)

dev_team_app = graph.compile()

config = {"recursion_limit": 50,
    "callbacks": [langfuse_handler],
    "metadata": {
            "langfuse_user_id": user_id,
            "langfuse_session_id": session_id,
            "langfuse_tags": tags
        }}

print("✅ Planner-Coder-Reviewer graph compiled")

# Test planner
"""
result = planner.invoke(
    {"messages": [{"role": "user", "content": "Write a SQL query to get the total number of employees"}]},
    {"recursion_limit": 50,
    "callbacks": [langfuse_handler],
    "metadata": {
            "langfuse_user_id": user_id,
            "langfuse_session_id": session_id,
            "langfuse_tags": tags
        },
    "configurable": {
            "thread_id": "test_planner_thread_1" # You can use any string (e.g., uuid) for the thread_id
        }
    },
)
"""

"""
# Run the team
result = dev_team_app.invoke(
    {"messages": [{"role": "user", "content": "Write a SQL query to get the total number of current working employees and average salary by year when they started working in the company"}]},
    {"recursion_limit": 50,
    "callbacks": [langfuse_handler],
    "metadata": {
            "langfuse_user_id": user_id,
            "langfuse_session_id": session_id,
            "langfuse_tags": tags
        }},
)
"""

def print_tool_call(tool_name, tool_args, indent=""):
    tool_args = tool_args[:tool_preview_len] + "..." if len(tool_args) > tool_preview_len else tool_args
    print(f"{indent}🔧 Tool called -> {tool_name}({tool_args})")

    tool_name = tool_registry.get(tool_name)
    if tool_name is None:
        print(f"{indent}❌ Unknown tool: {tool_name}")

def print_agent_step(msg):
    """Parses a single LangChain message object and prints it in a clean format."""
    indent = "    "

    msg_type = getattr(msg, "type", None)
    msg_content = getattr(msg, "content", "")

    if msg_type == "ai":
        
        tool_calls = getattr(msg, "tool_calls", [])
        if tool_calls:
            for tool_call in tool_calls:
                if isinstance(tool_call, dict):
                    tool_name = tool_call.get("name")
                    tool_args = str(tool_call.get("args"))
                else:
                    tool_name = getattr(tool_call, "name", "Unknown")
                    tool_args = str(getattr(tool_call, "args", "{}"))
                if tool_name:
                    print_tool_call(tool_name,tool_args,indent=indent)

    elif msg_type == "tool":
        tool_name = getattr(msg, "name", "unknown_tool")
        content_str = str(msg_content)

        print(f"{indent}✅ Result ({tool_name}):")
        formatted_name = tool_name.replace("_", " ").title()
        lines = content_str.splitlines()
        indented_content = "\n".join(f"{indent}│ {line}" for line in lines)
        print(f"\n{indent}╭─── 📄 {formatted_name} {'─' * (40 - len(formatted_name))}")
        print(indented_content)
        print(f"{indent}╰{'─' * 46}\n")

def main():
    print("SQL / DWH Assistant")
    print("type 'exit' or 'quit' to quit")
    print("-" * 100)

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

                for step in dev_team_app.stream(
                    current_input,
                    config=config
                ):
                    for update in step.values():
                        #print(update)

                        # HITL
                        if isinstance(update, tuple) and len(update) > 0 and isinstance(update[0], Interrupt):
                            interrupt = update[0]
                            interrupted = True
                
                            print(f"\n{'=' * 60}")
                            print(f" ⏸️  ACTION REQUIRES APPROVAL")
                            print(f"{'=' * 60}")

                        # usual agent messages
                        elif isinstance(update, dict):
                            for message in update.get("messages", []):
                                print_agent_step(message)

                    if interrupted:
                        break

                if not interrupted:
                    break

        except Exception as e:
            print(f"\n❌ An error occurred: {e}. Try again or type 'continue' (Don't worry, model remembers conversation with you!")

if __name__ == "__main__":
    main()