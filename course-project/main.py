from langchain.agents import create_agent
from langchain_core.tools import tool
from langgraph.graph import StateGraph, MessagesState, START, END
from typing import Literal
from agents.planner import planner
from agents.coder import coder
from agents.reviewer import reviewer
from dotenv import load_dotenv
from langfuse import get_client
from langfuse.langchain import CallbackHandler
from datetime import datetime
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

Використовуйте structured output для комунікації між агентами (Pydantic models, JSON schemas)
Давайте агентам різні моделі під задачу: потужну для planning/evaluation, дешевшу для execution

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
# агентів coder та critic винести в окремі файли, продумати тули, написати для них системні промпти

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

# Run the team
result = dev_team_app.invoke(
    {"messages": [{"role": "user", "content": "Write a SQL query to get the total number of current employees by year when they started working in the company"}]},
    {"recursion_limit": 50,
    "callbacks": [langfuse_handler],
    "metadata": {
            "langfuse_user_id": user_id,
            "langfuse_session_id": session_id,
            "langfuse_tags": tags
        }},
)

for msg in result["messages"][1:]:  # skip the user message
    name = getattr(msg, "name", msg.type)
    print(f"\n{'='*60}")
    print(f"🤖 {name}:")
    print(msg.content)
