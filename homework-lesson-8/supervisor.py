from langchain_core.tools import tool
from agents.planner import planner_agent
from agents.critic import critic_agent
from agents.research import research_agent
from config import ( 
    FINAL_PROMPT_research,
    FINAL_PROMPT_critic,
    FINAL_PROMPT_planner,
    max_iterations_planner,
    max_iterations_research,
    max_iterations_critic,
    revision_counter_max
)
from tools import save_report, tool_registry
from langgraph.errors import GraphRecursionError
from langchain.agents.middleware.tool_call_limit import ToolCallLimitExceededError
import uuid

revision_counter = 0
global current_research_session
current_research_session = str(uuid.uuid4())

# prompt idea for testing
"""
best ways to write system prompts for multi-agentic llm system which consists of 3 agents (business analyst, developer, and reviewer) and is designed to automate Power BI reports visual layer development using new pbir format
"""

# розібратися з варіантом edit - може тут викликати research
"""
        if choice == "approve":
            cmd = Command(resume={"decisions": [{"type": "approve"}]})
        elif choice == "reject":
            reason = input("Причина (опційно): ").strip() or "User rejected save_report"
            cmd = Command(
                resume={"decisions": [{"type": "reject", "message": reason}]}
            )
        else:
            fb = input("✏️  Ваш фідбек (буде додано до кінця звіту перед повторним збереженням): ").strip()
"""
# перевірити чи працює HITL з усіма опціями
# чекнути повторювані помилки
"""
✅ Result (knowledge_search): Error searching local knowledge base. Details: 'RustBindingsAPI' object has no attribute 'bindings'.
    ✅ Result (knowledge_search): Error searching local knowledge base. Details: 'index'.
або
✅ Result (knowledge_search): Error searching local knowledge base. Details: Could not connect to tenant default_tenant. Are you sure it exists?.
"""


def print_tool_call(tool_name, tool_args, indent=""):
    message_len = 150
    tool_args = tool_args[:message_len] + "..." if len(tool_args) > message_len else tool_args
    print(f"{indent}🔧 Tool called -> {tool_name}({tool_args})")

    tool_name = tool_registry.get(tool_name)
    if tool_name is None:
        print(f"{indent}❌ Unknown tool: {tool_name}")

def print_agent_step(msg, agent_name="Supervisor"):
    """Parses a single LangChain message object and prints it in a clean format."""
    indent = "    " if agent_name != "Supervisor" else ""

    msg_type = getattr(msg, "type", None)
    msg_content = getattr(msg, "content", "")

    if msg_type == "ai":
        if msg_content and agent_name == "Supervisor":
            print(f"\n{indent}🤖 Agent:\n{msg_content}")
        
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
        message_len = len(content_str) if tool_name in ["plan","research","critique"] else 150 
        preview = content_str[:message_len] + "..." if len(content_str) > message_len else content_str
        if tool_name in ["plan","research","critique"]:

            print(f"{indent}✅ Result ({tool_name}):")
            formatted_name = tool_name.replace("_", " ").title()
            lines = content_str.splitlines()
            if tool_name == "research":
                indented_content = "\n".join(f"{indent}│ {line}" for line in lines[:25])
                if len(lines) > 25:
                    indented_content += f"\n{indent}│ ... (25/{len(lines)} rows) ..."
            else:
                indented_content = "\n".join(f"{indent}│ {line}" for line in lines)
            print(f"\n{indent}╭─── 📄 {formatted_name} {'─' * (40 - len(formatted_name))}")
            print(indented_content)
            print(f"{indent}╰{'─' * 46}\n")

        else:
            print(f"{indent}✅ Result ({tool_name}): {preview}")

def run_agent_with_recovery(agent, request: str, config: dict, final_prompt: str, agent_name: str):
    indent = "    " if agent_name != "Supervisor" else ""
    
    try:
        for step in agent.stream(
            {"messages": [{"role": "user", "content": request}]},
            config=config
        ):
            for update in step.values():
                if isinstance(update, dict):
                    for message in update.get("messages", []):
                        print_agent_step(message, agent_name=agent_name)

        current_state = agent.get_state(config)
        result = current_state.values
        
        # Pydantic structured response
        if "structured_response" in result and result["structured_response"]:
            return result["structured_response"]
        # simplified fallback: raw text
        messages = result.get("messages", [])
        if messages and hasattr(messages[-1], "content") and messages[-1].content:
            return messages[-1].content
        return None
        
    except (GraphRecursionError, ToolCallLimitExceededError) as e:
        print(f"{indent}⚠️ Agent {agent_name} stopped: Reached max iterations. Forcing final output...")
        
        current_state = agent.get_state(config)
        recovery_config = config.copy()
        # Increase the limit slightly to allow one last "Final Prompt" pass
        recovery_config["recursion_limit"] = config["recursion_limit"] + 5

        messages = current_state.values.get("messages", [])
        recovery_messages = []
        
        if messages and hasattr(messages[-1], "tool_calls") and messages[-1].tool_calls:
            for tc in messages[-1].tool_calls:
                recovery_messages.append({
                    "role": "tool",
                    "tool_call_id": tc["id"],
                    "name": tc["name"],
                    "content": "System Abort: Tool execution cancelled because iteration limit was reached."
                })             
        recovery_messages.append({"role": "user", "content": final_prompt})
   
        try:
            final_result = agent.invoke(
                {"messages": recovery_messages},
                config=recovery_config
            )
            
            if "structured_response" in final_result and final_result["structured_response"]:
                return final_result["structured_response"]
            messages = final_result.get("messages", [])
            if messages and hasattr(messages[-1], "content") and messages[-1].content:
                return messages[-1].content
            return None

        except Exception as inner_e:
            print(f"{indent}❌ {agent_name} failed during recovery: {inner_e}")
            return None
    except Exception as e:
        print(f"{indent}❌ {agent_name} encountered an unexpected error: {e}")
        return None

@tool
def plan(request: str) -> str:
    """Create structured, step-by-step research plans from user requests.

    Usage:
    - Break down a question or topic into an actionable research strategy
    - Formulate specific search queries and determine the best data sources (web vs. internal)
    - Define the optimal structure and formatting for a final research report

    Input: Natural language research topic or request
    (e.g., 'Create a plan to research the market impact of solid-state batteries')
    """
    print(f"\n╭{'─'*30}\n│   [Supervisor → Planner]\n╰{'─'*30}")

    unique_planner_thread_id = f"planner_internal_thread{uuid.uuid4()}"
    config = {
        "recursion_limit": max_iterations_planner, 
        "configurable": {"thread_id": unique_planner_thread_id}
    }

    plan = run_agent_with_recovery(
        agent=planner_agent, 
        request=request, 
        config=config,
        final_prompt=FINAL_PROMPT_planner,
        agent_name="Planner")

    return plan.model_dump_json(indent=2) if plan else "Error: Could not generate research plan."

@tool
def research(plan: str) -> str:
    """Execute deep-dive research and generate a comprehensive Markdown report.

    Usage:
    - Execute a structured research plan or answer a complex, multi-step query
    - Gather detailed facts, statistics, and deep context from full articles (not just search snippets)
    - Search across external web sources, internal databases, financial data, or academic articles
    - Find current information from the web
    - Look up company policies, contacts, or OKRs
    - Get summaries of internal documentation
    - Compile gathered findings into a final, well-formatted Markdown report

    Input: A specific research query or a detailed research plan generated by the Planner.
    (e.g., 'Execute this research plan: Goal is to analyze TSLA financials. Queries: ...')
    """
    print(f"\n╭{'─'*30}\n│   [Supervisor → Researcher]\n╰{'─'*30}")

    global current_research_session
    unique_researcher_thread_id = f"research_internal_thread{current_research_session}"
    config = {
        "recursion_limit": max_iterations_research, 
        "configurable": {"thread_id": unique_researcher_thread_id}
    }
    
    res = run_agent_with_recovery(
            agent=research_agent, 
            request=plan, 
            config=config,
            final_prompt=FINAL_PROMPT_research,
            agent_name="Researcher")

    if res and hasattr(res, 'research_output'):
        return res.research_output
    return "Error: Could not generate report."

@tool
def critique(findings: str) -> str:
    """Independently review, fact-check, and evaluate a drafted research report.

    Usage:
    - Verify if the findings in a drafted report are accurate, up-to-date, and supported by sources
    - Check if the research fully covers the user's original request (completeness)
    - Assess the logical structure of the drafted text
    - Get a final verdict (APPROVE or REVISE) along with specific actionable revision requests

    Input: A string containing BOTH the original user request and the drafted research report.
    (e.g., 'Original request: [Topic]. Draft report: [Markdown text...]')
    """
    print(f"\n╭{'─'*30}\n│   [Supervisor → Critic]\n╰{'─'*30}")

    global revision_counter
    revision_counter += 1

    if revision_counter > revision_counter_max:
        print(f"\n⚠️ Critic Tool: Reached maximum revisions ({revision_counter}). Forcing APPROVE without calling agent.")
        import json
        mock_critique = {
            "verdict": "APPROVE",
            "is_fresh": True,
            "is_complete": True,
            "is_well_structured": True,
            "strengths": ["Achieved max number of iterations. Report is approved"],
            "gaps": ["No gaps"],
            "revision_requests": ["Achieved max number of iterations. Report is approved, it is the final version, save it."]
        }
        return f"--- CRITIQUE ROUND {revision_counter}/{revision_counter_max} ---\n" + json.dumps(mock_critique, indent=2)

    unique_critic_thread_id = f"critic_internal_thread{uuid.uuid4()}"
    config = {
        "recursion_limit": max_iterations_critic, 
        "configurable": {"thread_id": unique_critic_thread_id}
    }

    critique = run_agent_with_recovery(
        agent=critic_agent, 
        request=findings,
        config=config,
        final_prompt=FINAL_PROMPT_critic,
        agent_name="Critic")

    if not critique:
        return f"--- CRITIQUE ROUND {revision_counter}/{revision_counter_max} ---\n Error: Could not generate response."

    return f"--- CRITIQUE ROUND {revision_counter}/{revision_counter_max} ---\n" + critique.model_dump_json(indent=2)

tool_registry.update({
    "plan": plan,
    "research": research,
    "critique": critique
})