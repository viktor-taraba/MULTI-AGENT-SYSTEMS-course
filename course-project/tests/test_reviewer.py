from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from deepeval import assert_test
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.reviewer import reviewer as reviewer_agent
from config import LLM_test

reviewer_schema_compliance = GEval(
    name="Reviewer Output Schema Compliance",
    evaluation_steps=[
        "Check that 'verdict' is strictly exactly 'APPROVED' or 'REVISION_NEEDED'.",
        "Check that 'issues' is a list of strings.",
        "Check that 'suggestions' is a list of strings.",
        "Check that 'score' is a float between 0.0 and 1.0 inclusive.",
        "If verdict is 'APPROVED', 'issues' and 'suggestions' should be empty lists.",
        "If verdict is 'REVISION_NEEDED', 'issues' and 'suggestions' should contain at least one item."
    ],
    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
    model=LLM_test,
    threshold=0.9,
)

reviewer_bug_detection = GEval(
    name="Bug and Edge Case Detection",
    evaluation_steps=[
        "Analyze the SQL code provided in the input.",
        "Check if the reviewer correctly identified critical SQL flaws, such as missing NULLIF() around division denominators to prevent divide-by-zero errors.",
        "Check if the reviewer accurately flagged any missing JOINs or incorrect aggregations that violate the provided requirements."
    ],
    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
    model=LLM_test,
    threshold=0.8,
)

reviewer_spec_alignment = GEval(
    name="Specification Adherence Validation",
    evaluation_steps=[
        "Compare the 'Acceptance Criteria' in the input against the provided 'SQL Code'.",
        "Check if the reviewer explicitly caught when the SQL code omitted a required WHERE clause or filtering condition.",
        "Check that the reviewer enforced the exact output column names requested in the spec."
    ],
    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
    model=LLM_test,
    threshold=0.8,
)

reviewer_actionable_feedback = GEval(
    name="Actionable Feedback Quality",
    evaluation_steps=[
        "If the code has issues, check that the 'suggestions' field provides specific, concrete SQL syntax fixes (e.g., 'Use NULLIF(col, 0)', 'Add WHERE YEAR(date) = 2023').",
        "Check that the suggestions are not vague (e.g., 'Fix the error' is bad; 'Change INNER JOIN to LEFT JOIN' is good)."
    ],
    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
    model=LLM_test,
    threshold=0.7,
)

def test_reviewer_schema_compliance_approved():
    user_input = """
    SPECIFICATIONS:
    Requirements: Get total sales amount.
    Acceptance Criteria: Return one column named TotalSales.
    
    SQL CODE TO REVIEW:
    SELECT SUM(LineTotal) AS TotalSales FROM Sales.SalesOrderDetail;
    """
    agent_response = reviewer_agent.invoke(
            {"messages": [("user", user_input)]}, 
            config={"configurable": {"thread_id": "test_reviewer_001"}}
        )
    actual_output_str = str(agent_response.get("messages", [])[-1].content)

    test_case = LLMTestCase(
        input=user_input,
        actual_output=actual_output_str
    )
    assert_test(test_case, [reviewer_schema_compliance])


def test_reviewer_bug_detection_divide_by_zero():
    # potential divide-by-zero error
    user_input = """
    SPECIFICATIONS:
    Requirements: Calculate the order conversion rate (Total Orders / Total Website Visits) by territory.
    Acceptance Criteria: Return TerritoryID and ConversionRate.
    
    SQL CODE TO REVIEW:
    SELECT 
        TerritoryID,
        (SUM(TotalOrders) / SUM(TotalVisits)) AS ConversionRate
    FROM Sales.SalesTerritory
    GROUP BY TerritoryID;
    """
    agent_response = reviewer_agent.invoke(
            {"messages": [("user", user_input)]}, 
            config={"configurable": {"thread_id": "test_reviewer_002"}}
        )
    actual_output_str = str(agent_response.get("messages", [])[-1].content)

    test_case = LLMTestCase(
        input=user_input,
        actual_output=actual_output_str
    )
    # Testing both bug detection and making sure feedback is actionable
    assert_test(test_case, [reviewer_bug_detection, reviewer_actionable_feedback])


def test_reviewer_spec_alignment_missing_filter():
    # coder ignores an acceptance criterion (missing the 2013 date filter)
    user_input = """
    SPECIFICATIONS:
    Requirements: Get total revenue for 'Bikes' in the year 2013.
    Acceptance Criteria: 
    - Must return CategoryName, TotalRevenue.
    - Filter by OrderDate year = 2013.
    - Filter by ProductCategory.Name = 'Bikes'.
    
    SQL CODE TO REVIEW:
    SELECT 
        pc.[Name] AS CategoryName,
        SUM(sod.LineTotal) AS TotalRevenue
    FROM Sales.SalesOrderHeader soh
    JOIN Sales.SalesOrderDetail sod ON soh.SalesOrderID = sod.SalesOrderID
    JOIN Production.Product p ON sod.ProductID = p.ProductID
    JOIN Production.ProductSubcategory psc ON p.ProductSubcategoryID = psc.ProductSubcategoryID
    JOIN Production.ProductCategory pc ON psc.ProductCategoryID = pc.ProductCategoryID
    WHERE pc.[Name] = 'Bikes'
    GROUP BY pc.[Name];
    """
    
    agent_response = reviewer_agent.invoke(
            {"messages": [("user", user_input)]}, 
            config={"configurable": {"thread_id": "test_reviewer_003"}}
        )
    actual_output_str = str(agent_response.get("messages", [])[-1].content)

    test_case = LLMTestCase(
        input=user_input,
        actual_output=actual_output_str
    )
    assert_test(test_case, [reviewer_spec_alignment, reviewer_actionable_feedback])

    # deepeval test run tests/test_reviewer.py