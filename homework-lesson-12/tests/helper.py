import pytest

def extract_output_and_context(agent_response, stuctured_name, context_needed = True):
    """(helper function) safe answer extraction"""

    if "structured_response" in agent_response:
        actual_output_str = getattr(agent_response["structured_response"], stuctured_name, "")
    else:
        actual_output_str = str(agent_response.get("messages", [])[-1].content)

    if context_needed:
        context_list = [
            str(msg.content) 
            for msg in agent_response.get("messages", []) 
            if type(msg).__name__ == "ToolMessage"
        ]
    else:
        context_list = []

    return actual_output_str, context_list

def evaluate_and_assert(metric, function_name, threshold_name):
    """(helper function) prints for test results"""
    
    metric_name = getattr(metric, "name", metric.__class__.__name__)
    if metric.is_successful():
        print(f"\n✅ {function_name} ({metric_name}: {metric.score}, threshold: {metric.threshold})")
    else:
        print(f"\n❌ {function_name} ({metric_name}: {metric.score}, threshold: {metric.threshold})")
        print(f"   Reason: {metric.reason}")
        pytest.fail(f"DeepEval {threshold_name} threshold not met.")

def get_unique_tool_names(agent_response):
    """(helper function) extracts unique tool names from agent response"""

    unique_tool_names = []
    for msg in agent_response.get("messages", []):
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            for tool_call in msg.tool_calls:
                name = tool_call["name"]
                if name not in unique_tool_names:
                    unique_tool_names.append(name)

    return unique_tool_names