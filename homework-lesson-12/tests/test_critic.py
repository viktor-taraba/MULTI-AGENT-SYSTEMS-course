from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from deepeval import assert_test
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.critic import critic_agent

critique_quality = GEval(
    name="Critique Quality",
    evaluation_steps=[
        "Check that the critique identifies specific issues, not vague complaints",
        "Check that revision_requests are actionable (researcher can act on them)",
        "If verdict is APPROVE, gaps list should be empty or contain only minor items",
        "If verdict is REVISE, there must be at least one revision_request",
    ],
    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
    model="gpt-5.4-mini",
    threshold=0.7,
)

def test_critique_approve():
    with open("tests/critic_tests_examples/pbir_multi_agent_prompting_report.md", "r", encoding="utf-8") as f:
        approve_report = f.read()

    user_input = f"Review report: {approve_report}"
    agent_response = critic_agent.invoke(
            {"messages": [("user", user_input)]}, 
            config={"configurable": {"thread_id": "test_thread_001"}}
        )
    actual_output_str = str(agent_response.get("messages", [])[-1].content)
        
    test_case = LLMTestCase(
        input=user_input,
        actual_output=actual_output_str
    )
    assert_test(test_case, [critique_quality])

def test_critique_revise():
    with open("tests/critic_tests_examples/ponziani_opening_report.md", "r", encoding="utf-8") as f:
        revise_report = f.read()

    user_input = f"Review report: {revise_report}"
    agent_response = critic_agent.invoke(
            {"messages": [("user", user_input)]}, 
            config={"configurable": {"thread_id": "test_thread_002"}}
        )
    actual_output_str = str(agent_response.get("messages", [])[-1].content)
        
    test_case = LLMTestCase(
        input=user_input,
        actual_output=actual_output_str
    )
    assert_test(test_case, [critique_quality])