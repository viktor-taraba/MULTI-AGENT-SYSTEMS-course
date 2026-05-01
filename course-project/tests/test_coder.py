from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from deepeval import assert_test
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.coder import coder as coder_agent
from config import LLM_test

code_schema_compliance = GEval(
    name="Code Output Schema Compliance",
    evaluation_steps=[
        "Check that the output contains a 'source_code' field with the actual code.",
        "Check that the output contains a 'description' field with a text explanation.",
        "Check that the output contains a 'files_created' field formatted as a list of strings (e.g., filenames with extensions like .sql).",
    ],
    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
    model=LLM_test,
    threshold=0.9,
)

code_sql_best_practices = GEval(
    name="SQL Code Quality and Best Practices",
    evaluation_steps=[
        "Check that the 'source_code' is written in T-SQL dialect.",
        "Check that the SQL code includes inline comments (using -- or /* */) explaining complex logic or decisions.",
        "Check that the code uses proper indentation and formatting for readability.",
        "If the query involves multiple steps, subqueries, or complex joins, check that it utilizes Common Table Expressions (CTEs / 'WITH' clauses) rather than deeply nested subqueries."
    ],
    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
    model=LLM_test,
    threshold=0.7,
)

code_description_quality = GEval(
    name="Code Description Completeness",
    evaluation_steps=[
        "Check that the 'description' field is not just a single vague sentence.",
        "Check that the description explicitly mentions the core algorithm or logic used in the SQL query.",
        "Check that the description details the main tables being joined or queried.",
        "Check that the description highlights at least one key architectural decision or data handling rule applied in the code."
    ],
    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
    model=LLM_test,
    threshold=0.7,
)

code_logic_alignment = GEval(
    name="Code Logic Alignment with Requirements",
    evaluation_steps=[
        "Analyze the input specification (requirements and acceptance criteria).",
        "Check that the generated 'source_code' contains the necessary SELECT statements, JOINs, and / or WHERE clauses to fulfill the specific input requirements.",
        "Check that the code does NOT contain placeholder table names or column names (like 'your_table_here'), implying the agent attempted to use schema tools or write production-ready code."
    ],
    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
    model=LLM_test,
    threshold=0.8,
)

def test_code_schema_compliance():
    user_input = """
    Title: Get Total Sales by Region
    Requirements: Join Sales and Region tables. Sum the SalesAmount. Group by RegionName.
    Acceptance Criteria: Returns RegionName and TotalSales. No null regions.
    """
    agent_response = coder_agent.invoke(
            {"messages": [("user", user_input)]}, 
            config={"configurable": {"thread_id": "test_coder_001"}}
        )
    actual_output_str = str(agent_response.get("messages", [])[-1].content)

    test_case = LLMTestCase(
        input=user_input,
        actual_output=actual_output_str
    )
    assert_test(test_case, [code_schema_compliance])

def test_code_sql_best_practices():
    user_input = """
    Title: Identify Top Performing Employees by Department
    Requirements: Find the employee with the highest sales in each department for the last year available. 
    Acceptance Criteria: Use window functions (e.g., ROW_NUMBER) to partition by department. Return EmployeeName, DepartmentName, and TotalSales.
    """
    agent_response = coder_agent.invoke(
            {"messages": [("user", user_input)]}, 
            config={"configurable": {"thread_id": "test_coder_002"}}
        )
    actual_output_str = str(agent_response.get("messages", [])[-1].content)

    test_case = LLMTestCase(
        input=user_input,
        actual_output=actual_output_str
    )
    assert_test(test_case, [code_sql_best_practices])

def test_code_description_quality():
    user_input = """
    Title: 2013 Bike Sales Performance
    Requirements: Calculate the total revenue and total quantity sold for all products in the 'Bikes' category during the year 2013. You must join SalesOrderHeader, SalesOrderDetail, Product, ProductSubcategory, and ProductCategory.
    Acceptance Criteria: 
    - Must return CategoryName, TotalRevenue (based on LineTotal), and TotalQuantity (based on OrderQty). 
    - Filter by OrderDate year = 2013. 
    - Filter by ProductCategory.Name = 'Bikes'.
    """
    agent_response = coder_agent.invoke(
            {"messages": [("user", user_input)]}, 
            config={"configurable": {"thread_id": "test_coder_003"}}
        )
    actual_output_str = str(agent_response.get("messages", [])[-1].content)

    test_case = LLMTestCase(
        input=user_input,
        actual_output=actual_output_str
    )
    assert_test(test_case, [code_description_quality])

def test_code_logic_alignment():
    user_input = """
    Title: Retrieve Active Products without Sales
    Requirements: Select all products from the Production.Product table where IsActive = 1, but they do not exist in the Sales.SalesOrderDetail table for the current year.
    Acceptance Criteria: Must use a LEFT JOIN or NOT EXISTS logic. Ensure IsActive filter is applied.
    """
    agent_response = coder_agent.invoke(
            {"messages": [("user", user_input)]}, 
            config={"configurable": {"thread_id": "test_coder_004"}}
        )
    actual_output_str = str(agent_response.get("messages", [])[-1].content)

    test_case = LLMTestCase(
        input=user_input,
        actual_output=actual_output_str
    )
    assert_test(test_case, [code_logic_alignment])

# deepeval test run tests/test_coder.py