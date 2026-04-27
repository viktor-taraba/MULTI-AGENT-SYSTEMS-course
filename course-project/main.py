from langchain.agents import create_agent
from langchain_core.tools import tool
from langgraph.graph import StateGraph, MessagesState, START, END
from pydantic import BaseModel
from typing import Literal
from dotenv import load_dotenv
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
"""

# Planner-Coder-Reviewer team as a LangGraph graph

LLM_POWERFUL = "openai:gpt-5.4"       # for planning, evaluation, supervision
LLM_FAST = "openai:gpt-5.4-nano"     # for execution, simple tasks

@tool
def write_file(path: str, content: str) -> str:
    """Write content to a file."""
    return f"File {path} written successfully."

@tool
def run_tests(path: str) -> str:
    """Run tests for a file."""
    return "All tests passed."

# Define agents with different model tiers
planner = create_agent(
    model=LLM_POWERFUL,
    tools=[],
    system_prompt=(
        "You are a software architect. Given a task, break it into 2-3 concrete implementation steps. "
        "Be concise — just a numbered list."
    ),
    name="planner",
)

coder = create_agent(
    model=LLM_FAST,
    tools=[write_file, run_tests],
    system_prompt="You are a Python developer. Implement the plan step by step. Be concise.",
    name="coder",
)

reviewer = create_agent(
    model=LLM_POWERFUL,
    tools=[],
    system_prompt=(
        "You are a code reviewer. Check code for bugs and plan compliance. "
        "If issues found, say REVISION_NEEDED and list problems. "
        "If code is good, say APPROVED."
    ),
    name="reviewer",
)

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

# Run the team
result = dev_team_app.invoke(
    {"messages": [{"role": "user", "content": "Create a Python function to check if a number is prime"}]},
    {"recursion_limit": 25},
)

# Print each agent's contribution
for msg in result["messages"][1:]:  # skip the user message
    name = getattr(msg, "name", msg.type)
    print(f"\n{'='*60}")
    print(f"🤖 {name}:")
    print(msg.content)
