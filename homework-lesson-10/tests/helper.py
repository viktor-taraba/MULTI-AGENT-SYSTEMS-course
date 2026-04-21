import pytest

def extract_output_and_context(agent_response, stuctured_name):
    """(helper function) safe answer extraction"""

    if "structured_response" in agent_response:
        actual_output_str = getattr(agent_response["structured_response"], stuctured_name, "")
    else:
        actual_output_str = str(agent_response.get("messages", [])[-1].content)

    context_list = [
        str(msg.content) 
        for msg in agent_response.get("messages", []) 
        if type(msg).__name__ == "ToolMessage"
    ]

    return actual_output_str, context_list

def evaluate_and_assert(metric, function_name, threshold_name):
    """(helper function) prints for test results"""

    if metric.is_successful():
        print(f"\n✅ {function_name} ({metric.name}: {metric.score}, threshold: {metric.threshold})")
    else:
        print(f"\n❌ {function_name} ({metric.name}: {metric.score}, threshold: {metric.threshold})")
        print(f"   Reason: {metric.reason}")
        pytest.fail(f"DeepEval {threshold_name} threshold not met.")