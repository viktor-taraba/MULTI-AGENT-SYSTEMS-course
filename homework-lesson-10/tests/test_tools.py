from deepeval.test_case import LLMTestCase, ToolCall
from deepeval.metrics import ToolCorrectnessMetric

# Planner should use web_search and/or knowledge_search for exploration
# Researcher should use web_search, read_url, knowledge_search
# Critic should verify facts via web_search

tool_metric = ToolCorrectnessMetric(threshold=0.5, model="gpt-5.4-mini")

"""
Створіть мінімум 3 тест-кейси для tool correctness:

Planner отримує запит → має викликати пошукові інструменти
Researcher отримує план → має використати інструменти згідно з sources_to_check
Supervisor отримує APPROVE від Critic → має викликати save_report
"""

def test_planner_tools():
    pass

def test_researcher_tools():
    pass

def test_supervisor_save():
    pass