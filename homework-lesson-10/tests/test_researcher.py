from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from agents.research import research_agent
import pytest

# тут додати те ж саме що в планері
# написати спрощену версію тесту з FaithfulnessMetric для RAG

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

edge_case_fictional = GEval(
    name="No Hallucination",
    evaluation_steps=[
        "Read the user's input, which is a deliberate request for a fictional or impossible topic.",
        "Check the 'actual output'. It MUST explicitly state that no credible information could be found.",
        "If the 'actual output' invents facts, historical events, or scientific data about the fictional topic, the score must be 0.",
        "Reward the output if it remains polite, objective, and refuses to hallucinate."
    ],
    evaluation_params=[
        LLMTestCaseParams.INPUT,
        LLMTestCaseParams.ACTUAL_OUTPUT,
    ],
    model="gpt-5.4-mini",
    threshold=0.8,
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
"""
def test_research_grounded():
    # загорнути потім у функцію
    user_input = "Create a short report on the PBIR format files and structure (Power BI)."
    agent_response = research_agent.invoke(
            {"messages": [("user", user_input)]}, 
            config={"configurable": {"thread_id": "test_thread_001"}}
        )

    if "structured_response" in agent_response:
        actual_output_str = getattr(agent_response["structured_response"], "research_output", "")
    else:
        actual_output_str = str(agent_response.get("messages", [])[-1].content)

    context_list = [
        str(msg.content) 
        for msg in agent_response.get("messages", []) 
        if type(msg).__name__ == "ToolMessage"
    ]

    # to delete
    print()
    print("---"*60)
    print(actual_output_str)
    print("---"*60)
    print(str(context_list))
    print("---"*60)
    print()

    test_case = LLMTestCase(
        input=user_input,
        actual_output=actual_output_str,
        retrieval_context = context_list
    )
    groundedness.measure(test_case)

    # це теж загорнути як окрему ф-ю
    if groundedness.is_successful():
        print(f"\n✅ test_research_grounded ({groundedness.name}: {groundedness.score}, threshold: {groundedness.threshold})")
    else:
        print(f"\n❌ test_research_grounded ({groundedness.name}: {groundedness.score}, threshold: {groundedness.threshold})")
        print(f"   Reason: {groundedness.reason}")
        pytest.fail("DeepEval groundedness threshold not met.")
"""
def test_research_edge_case():
    # загорнути потім у функцію
    user_input = "The 2025 Saharan Spheniscidae Expedition: Assessing Avian Desert Adaptation"
    agent_response = research_agent.invoke(
            {"messages": [("user", user_input)]}, 
            config={"configurable": {"thread_id": "test_thread_002"}}
        )

    if "structured_response" in agent_response:
        actual_output_str = getattr(agent_response["structured_response"], "research_output", "")
    else:
        actual_output_str = str(agent_response.get("messages", [])[-1].content)

    context_list = [
        str(msg.content) 
        for msg in agent_response.get("messages", []) 
        if type(msg).__name__ == "ToolMessage"
    ]

    # to delete
    print()
    print("---"*60)
    print(actual_output_str)
    print("---"*60)
    print(str(context_list))
    print("---"*60)
    print()

    test_case = LLMTestCase(
        input=user_input,
        actual_output=actual_output_str,
        retrieval_context = context_list
    )
    edge_case_fictional.measure(test_case)

    # це теж загорнути як окрему ф-ю
    if edge_case_fictional.is_successful():
        print(f"\n✅ test_research_grounded ({edge_case_fictional.name}: {edge_case_fictional.score}, threshold: {edge_case_fictional.threshold})")
    else:
        print(f"\n❌ test_research_grounded ({edge_case_fictional.name}: {edge_case_fictional.score}, threshold: {edge_case_fictional.threshold})")
        print(f"   Reason: {edge_case_fictional.reason}")
        pytest.fail("DeepEval groundedness threshold not met.")

# python -m pytest tests/test_researcher.py -v -s --tb=short -W ignore::DeprecationWarning