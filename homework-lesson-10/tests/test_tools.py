from deepeval.test_case import LLMTestCase, ToolCall
from deepeval.metrics import ToolCorrectnessMetric
from agents.planner import planner_agent
from agents.research import research_agent
from langchain.agents.middleware.tool_call_limit import ToolCallLimitExceededError
from helper import evaluate_and_assert, get_unique_tool_names

# Critic should verify facts via web_search

tool_correctness_metric = ToolCorrectnessMetric(threshold=0.7, model="gpt-5.4-mini")

"""
Створіть мінімум 3 тест-кейси для tool correctness:

Planner отримує запит → має викликати пошукові інструменти
Researcher отримує план → має використати інструменти згідно з sources_to_check
Supervisor отримує APPROVE від Critic → має викликати save_report
"""

def test_planner_tools():
    user_input = "Create a research plan for agentic development for MS Power BI"
    agent_response = planner_agent.invoke(
            {"messages": [("user", user_input)]}, 
            config={"configurable": {"thread_id": "test_thread_001"}}
        )

    unique_tool_names = get_unique_tool_names(agent_response)

    test_case = LLMTestCase(
        input=user_input,
        actual_output="Plan ready",
        tools_called=[ToolCall(name=tool_name) for tool_name in unique_tool_names],
        expected_tools=[
            ToolCall(name="web_search"),
            ToolCall(name="knowledge_search")
        ],
    )
    tool_correctness_metric.measure(test_case)
    evaluate_and_assert(tool_correctness_metric, "test_planner_tools", "tool_correctness_metric")

def test_researcher_tools():
    user_input = """
      {
        "goal": "Create a concise, actionable high-level overview of the PBIR (Power BI enhanced report) structure for BI architects and report authors — covering purpose, components, file organization, key metadata fields, comparison to earlier Power BI formats (PBIX/PBIP), migration guidance, best practices, and security/validation considerations.",
        "search_queries": [
          "Power BI PBIR file format specification Microsoft blog \"PBIR\" \"Power BI enhanced report format\"",
          "PBIR vs PBIX vs PBIP differences \"PBIR will become the default\"",
          "PBIR file structure manifest metadata fields \"PBIR\" \"manifest\"",
          "Power BI PBIR migration guide \"migrate PBIX to PBIR\"",
          "Power BI PBIR security signing encryption validation \"PBIR\"",
          "Power BI Desktop developer mode PBIR developer preview release notes",
          "example PBIR file tree directory layout \"PBIR\" sample structure",
          "best practices PBIR report authors \"Power BI\""
        ],
        "sources_to_check": [
          "web_search",
          "read_url",
          "knowledge_search"
        ],
        "output_format": "A concise Markdown report for BI architects and report authors with these sections: 1) Executive summary (1 paragraph); 2) Purpose (1 short paragraph); 3) Components (bulleted list with 1-line descriptions for each component/file); 4) File organization (sample directory/tree code block + short explanation of each folder/file); 5) Key metadata fields (compact table: field name | type | purpose | required/optional); 6) Comparison to previous formats (2-column table: PBIR vs PBIX/PBIP highlighting key differences and impact areas); 7) Migration guidance (practical step-by-step checklist, common pitfalls, validation steps, estimated effort for typical reports); 8) Best practices (8–12 concise bullets for architects/report authors); 9) Security & validation considerations (checklist, tools, signing/permissions notes); 10) References & links (3–6 authoritative links) — prioritize clarity, actionable bullets, sample manifest snippets and a sample validation checklist. Final deliverable: a well-formatted, visually clear Markdown document suitable for immediate distribution to BI teams."
      }"""

    try:
        config={"configurable": {"thread_id": "test_thread_001"}}
        agent_response = research_agent.invoke(
                {"messages": [("user", user_input)]}, 
                config=config
            )
    except ToolCallLimitExceededError:
        current_state = research_agent.get_state(config)
        messages_list = current_state.values.get("messages", [])
        agent_response = {"messages": messages_list}

    unique_tool_names = get_unique_tool_names(agent_response)

    test_case = LLMTestCase(
        input=user_input,
        actual_output="Plan ready",
        tools_called=[ToolCall(name=tool_name) for tool_name in unique_tool_names],
        expected_tools=[
            ToolCall(name="web_search"),
            ToolCall(name="knowledge_search"),
            ToolCall(name="read_url")
        ],
    )
    tool_correctness_metric.measure(test_case)
    evaluate_and_assert(tool_correctness_metric, "test_researcher_tools", "tool_correctness_metric")

def test_supervisor_save():
    pass

# python -m pytest tests/test_tools.py -v -s --tb=short -W ignore::DeprecationWarning --show-capture=no