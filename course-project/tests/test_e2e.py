from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from deepeval import assert_test
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import LLM_test
from helper import run_e2e_graph

e2e_task_completion = GEval(
    name="Task Accuracy and Completion",
    evaluation_steps=[
        "Analyze the user's original request.",
        "Verify that the final SQL code completely solves the user's exact problem.",
        "Check that no requested filters, aggregations, or specific output columns were missed or ignored by the multi-agent system.",
        "Check that the final output does NOT contain any reviewer notes or intermediate planning steps; it should only be the final requested code/description."
    ],
    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
    model=LLM_test,
    threshold=0.8, 
)

e2e_production_readiness = GEval(
    name="Production SQL Quality",
    evaluation_steps=[
        "Check that the final SQL is syntactically valid T-SQL.",
        "Verify that the code demonstrates production-level defensive programming.",
        "Check that the SQL is well-formatted and includes explanatory inline comments.",
        "Ensure no placeholder schema names ('your_db.your_table') exist, proving the system utilized its schema tools correctly."
    ],
    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
    model=LLM_test,
    threshold=0.8,
)

e2e_query_efficiency = GEval(
    name="Query Efficiency",
    evaluation_steps=[
        "Check that the code explicitly selects necessary columns rather than using 'SELECT *'.",
        "Check that 'WHERE' clause filters are sargable (e.g., avoiding wrapping columns in functions like YEAR(date) = 2023, and preferring date >= '2023-01-01' AND date < '2024-01-01').",
        "Check that the query prefers JOINs over inherently slow correlated subqueries where possible.",
        "Check if appropriate aggregation functions are used efficiently without redundant grouping."
    ],
    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
    model=LLM_test,
    threshold=0.8,
)

e2e_security_safety = GEval(
    name="Security and Safety",
    evaluation_steps=[
        "Verify that the generated SQL contains ONLY read-only commands (SELECT).",
        "Ensure there are NO destructive Data Manipulation Language (DML) commands like INSERT, UPDATE, DELETE, or TRUNCATE.",
        "Ensure there are NO Data Definition Language (DDL) commands like DROP, ALTER, or CREATE.",
        "Check that the code does not execute dynamic SQL strings (e.g., using EXEC() or sp_executesql) unless explicitly requested."
    ],
    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
    model=LLM_test,
    threshold=1.0,
)

e2e_schema_hallucination = GEval(
    name="Schema Hallucination Free",
    evaluation_steps=[
        "Analyze the tables and columns used in the generated SQL.",
        "Verify that every table and column logically aligns with the explicit requirements provided in the user input.",
        "Flag any tables or columns that appear to be completely invented or generic placeholders (e.g., 'data_table', 'user_info') that were not specified in the prompt."
    ],
    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
    model=LLM_test,
    threshold=0.9,
)

e2e_maintainability = GEval(
    name="Maintainability",
    evaluation_steps=[
        "Check that all tables in JOINs have clear, concise aliases (e.g., 'SalesOrderHeader soh').",
        "Check that all calculated columns or aggregations have explicit aliases (using 'AS').",
        "Check that the code is structured cleanly with logical indentation for SELECT, FROM, WHERE, and JOIN clauses.",
        "Check the 'description' field of the output to ensure it accurately and clearly explains the technical intent of the query."
    ],
    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
    model=LLM_test,
    threshold=0.7,
)

metrics_list = [
        e2e_task_completion,
        e2e_production_readiness,
        e2e_query_efficiency,
        e2e_security_safety,
        e2e_schema_hallucination,
        e2e_maintainability]

def test_e2e_recent_hires():
    user_input = """
    Title: Most Recently Hired Employee per Department
    Requirements: Find the newest, currently active employee in each department. You must join HumanResources.Employee, HumanResources.EmployeeDepartmentHistory, HumanResources.Department, and Person.Person to get the actual names. 
    Acceptance Criteria:
    - Must return DepartmentName, FirstName, LastName, and HireDate.
    - Must filter EmployeeDepartmentHistory to only include current assignments (where EndDate IS NULL).
    - Must use a window function (like ROW_NUMBER) to partition by department and sort by HireDate descending.
    """
    actual_output_str = run_e2e_graph(user_input, "e2e_001")

    test_case = LLMTestCase(input=user_input, actual_output=actual_output_str)
    assert_test(test_case, metrics_list)

def test_e2e_aw_customers_without_orders():
    user_input = """
    Title: Registered Customers Without Orders
    Requirements: Identify all customers in the database who have an account but have never actually placed an order. You will need to check the Sales.Customer table against the Sales.SalesOrderHeader table.
    Acceptance Criteria:
    - Must return exactly one column: CustomerID.
    - Must use either a LEFT JOIN with a NULL check or a NOT EXISTS clause.
    - Ensure the result set does not include any customer who has placed an order.
    """
    actual_output_str = run_e2e_graph(user_input, "e2e_002")

    test_case = LLMTestCase(input=user_input, actual_output=actual_output_str)
    assert_test(test_case, metrics_list)

def test_e2e_high_reach_products():
    user_input = """
    Title: High-Reach Products
    Requirements: Find all products that have been sold to at least 50 distinct, unique customers. Calculate the total lifetime revenue for each of these high-reach products. You must join Production.Product, Sales.SalesOrderDetail, and Sales.SalesOrderHeader.
    Acceptance Criteria:
    - Must return ProductName, UniqueCustomerCount, and TotalLifetimeRevenue.
    - Must use COUNT(DISTINCT CustomerID) to determine the unique reach.
    - Must use a HAVING clause to filter out products with fewer than 50 unique customers.
    """
    actual_output_str = run_e2e_graph(user_input, "e2e_003")

    test_case = LLMTestCase(input=user_input, actual_output=actual_output_str)
    assert_test(test_case, metrics_list)

def test_e2e_yoy_revenue_growth():
    user_input = """
    Title: Year-Over-Year Revenue Growth by Territory
    Requirements: Calculate the total revenue per year for each sales territory, and then compare it to the previous year's revenue to find the growth percentage. You will need Sales.SalesOrderHeader and Sales.SalesTerritory.
    Acceptance Criteria:
    - Must return TerritoryName, SalesYear, CurrentYearRevenue, PreviousYearRevenue, and YoYGrowthPercentage.
    - Must use a CTE to first calculate the grouped annual revenue per territory.
    - Must use the LAG() window function to retrieve the previous year's revenue on the same row.
    - Must gracefully handle the first year (where previous year revenue is NULL).
    """
    actual_output_str = run_e2e_graph(user_input, "e2e_004")

    test_case = LLMTestCase(input=user_input, actual_output=actual_output_str)
    assert_test(test_case, metrics_list)

def test_e2e_email_domain_distribution():
    user_input = """
    Title: Email Domain Distribution
    Requirements: Analyze the Person.EmailAddress table to find out the most popular email domains (e.g., 'gmail.com', 'adventure-works.com') used by contacts in the database. 
    Acceptance Criteria:
    - Must return EmailDomain and DomainCount.
    - Must extract the domain from the EmailAddress column by finding the string after the '@' symbol using T-SQL string functions (like SUBSTRING and CHARINDEX).
    - Must group by the extracted domain and order the results from most frequent to least frequent.
    """
    actual_output_str = run_e2e_graph(user_input, "e2e_005")

    test_case = LLMTestCase(input=user_input, actual_output=actual_output_str)
    assert_test(test_case, metrics_list)

# deepeval test run tests/test_e2e.py