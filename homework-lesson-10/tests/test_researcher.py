from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from agents.research import research_agent
import pytest

# тут додати те ж саме що в планері
# FAILED tests/test_researcher.py::test_research_grounded - deepeval.errors.MissingTestCaseParamsError: 'retrieval_context' cannot be None for
#  the 'Groundedness [GEval]' metric
# тут окремо вичепити останнє повідомлення агента (звіт) і все що було до нього - контекст, але в більш читабельному вигляді, приміром як з принтами в консоль

groundedness = GEval(
    name="Groundedness",
    evaluation_steps=[
        "Extract every factual claim from 'actual output'",
        "For each claim, check if it can be directly supported by 'retrieval context'",
        "Claims not present in retrieval context count as ungrounded, even if true",
        "Score = number of grounded claims / total claims",
    ],
    evaluation_params=[
        LLMTestCaseParams.ACTUAL_OUTPUT,
        LLMTestCaseParams.RETRIEVAL_CONTEXT,
    ],
    model="gpt-5.4-mini",
    threshold=0.7,
)

def extract_actual_output(agent_response) -> str:
    """(helper function) safe answer extraction"""
    if hasattr(agent_response, "model_dump_json"):
        return agent_response.model_dump_json()
    return str(agent_response)

def evaluate_and_assert(metric, test_case):
    """(helper function) prints for test results"""
    metric.measure(test_case)
    if metric.is_successful():
        print(f"\n✅ {metric.name}: {metric.score} (threshold: {metric.threshold})")
    else:
        print(f"\n❌ {metric.name}: {metric.score} (threshold: {metric.threshold})")
        print(f"   Reason: {metric.reason}")
        pytest.fail(f"DeepEval threshold not met for {metric.name}.")

def test_research_grounded():
    # загорнути потім у функцію
    user_input = "Create a short report on the PBIR format files and structure (Power BI)."
    agent_response = research_agent.invoke(
            {"messages": [("user", user_input)]}, 
            config={"configurable": {"thread_id": "test_thread_001"}}
        )

    if hasattr(agent_response, "model_dump_json"):
        actual_output_str = agent_response.model_dump_json()
    else:
        actual_output_str = str(agent_response)

    # to delete
    print(actual_output_str)

    test_case = LLMTestCase(
        input=user_input,
        actual_output=actual_output_str
    )
    groundedness.measure(test_case)

    # це теж загорнути як окрему ф-ю
    if groundedness.is_successful():
        print(f"\n✅ test_research_grounded ({groundedness.name}: {groundedness.score}, threshold: {groundedness.threshold})")
    else:
        print(f"\n❌ test_research_grounded ({groundedness.name}: {groundedness.score}, threshold: {groundedness.threshold})")
        print(f"   Reason: {groundedness.reason}")
        pytest.fail("DeepEval groundedness threshold not met.")

def test_research_edge_case():
    pass

# python -m pytest tests/test_researcher.py -v -s --tb=short -W ignore::DeprecationWarning