from langchain_core.tools import tool
import trafilatura
import json
import io
import requests
import logging
from ddgs import DDGS
from config import (
    max_search_results, 
    max_url_content_length,
    server,
    database,
    timeout_seconds
    )
from typing import List, Dict
from pypdf import PdfReader
from retriever import get_retriever
from langgraph.types import interrupt
import sqlparse
import pyodbc

def validate_safe_sql(query: str) -> bool:
    """
    Helper function: Parses a SQL query and raises a ValueError if it contains 
    destructive or state-altering commands.
    Args:
        query (str): The SQL query string to evaluate.
    Returns:
        bool: True if the query is safe (read-only).
    Raises:
        ValueError: If a dangerous statement type is detected.
    """

    dangerous_commands = {
        'DELETE', 'DROP', 'TRUNCATE', 'ALTER', 'UPDATE', 
        'INSERT', 'GRANT', 'REVOKE', 'REPLACE', 'CREATE'
    }
    
    # Parse the query. sqlparse handles multiple statements separated by ';'
    parsed_statements = sqlparse.parse(query)
    
    for stmt in parsed_statements:
        command_type = stmt.get_type()
        if command_type in dangerous_commands:
            return f"Security Error: The AI attempted to use a forbidden. SQL command '{command_type}'."
            
    return True

@tool
def get_table_structure(table_name: str, schema_name: str) -> str:
    """
    Retrieves the column structure (name, data type, length, nullability, precision) of a specified DWH table.
    Use this tool when you need to understand the schema and data types of a table before writing queries or when ypu have suspicion that documentation is outdated.
    
    Args:
        table_name (str): The name of the table to inspect (e.g., 'Store').
        schema_name (str): The schema the table belongs to (e.g., 'Sales').
        
    Returns:
        str: Table structure details in JSON format (list of dictionaries) or an error message.
    """

    connection_string = f'''
        DRIVER={{ODBC Driver 17 for SQL Server}};
        SERVER={server};
        DATABASE={database};
        Trusted_Connection=yes;
    '''
    
    query = """
        SELECT 
            COLUMN_NAME, 
            DATA_TYPE, 
            CHARACTER_MAXIMUM_LENGTH AS MAX_LENGTH, 
            IS_NULLABLE, 
            NUMERIC_PRECISION,
            NUMERIC_SCALE
        FROM 
            INFORMATION_SCHEMA.COLUMNS 
        WHERE 
            TABLE_NAME = ? AND TABLE_SCHEMA = ?;
    """
    
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute(query, (table_name, schema_name))
        
        if cursor.description:
            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()
            
            if not rows:
                return json.dumps({
                    "status": "not_found", 
                    "message": f"Table '{schema_name}.{table_name}' not found or has no columns."
                })
                
            result_data = [dict(zip(columns, row)) for row in rows]
            return json.dumps(result_data, default=str)
        else:
            return json.dumps({"status": "error", "message": "Failed to retrieve metadata."})
            
    except pyodbc.Error as e:
        return json.dumps({"status": "error", "error_message": str(e)})
        
    finally:
        if 'conn' in locals():
            conn.close()

@tool
def execute_sql_query(query: str) -> str:
    """
    Executes a SQL query against a SQL Server database and returns the results.
    Use this tool when you need to retrieve data from the database, for example, information about departments (Department).
    
    Args:
        query (str): Formatted SQL query to execute (e.g., "SELECT * FROM [HumanResources].[Department]").
        
    Returns:
        str: Query results in JSON format (list of dictionaries) or an error message.
    """

    connection_string = f'''
        DRIVER={{ODBC Driver 17 for SQL Server}};
        SERVER={server};
        DATABASE={database};
        Trusted_Connection=yes;
    '''
    try:
        conn = pyodbc.connect(connection_string)
        conn.timeout = timeout_seconds
        cursor = conn.cursor()

        if validate_safe_sql:
            cursor.execute(query)
        
        if cursor.description:
            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()
            result_data = [dict(zip(columns, row)) for row in rows]
            return json.dumps(result_data, default=str)
        else:
            conn.commit()
            return json.dumps({"status": "success", "message": "Query executed successfully. No rows returned."})
            
    except pyodbc.Error as e:
        return json.dumps({"status": "error", "error_message": str(e)})
        
    finally:
        if 'conn' in locals():
            conn.close()

@tool
def ask_user_for_clarification(question: str) -> str:
    """
    Use this tool to ask the user a clarifying question BEFORE generating the final specification.
    Call this when the business requirements are ambiguous, missing, or need confirmation.
    
    Args:
        question (str): The precise question to ask the user.
    """
    human_answer = interrupt(f"🤔 PLANNER QUESTION: {question}")
    
    return human_answer

"""
SET SHOWPLAN_XML ON	Estimated	Returns the plan as XML without executing the query. Safe for large delete/update tests.
SET STATISTICS XML ON	Actual	Executes the query and returns the plan. Provides real-time metrics like actual row counts.
"""

def get_sql_execution_plan(query):
    """
    Retrieves the XML execution plan for a given SQL query.
    """
    plan_xml = ""
    connection_string = f'''
        DRIVER={{ODBC Driver 17 for SQL Server}};
        SERVER={server};
        DATABASE={database};
        Trusted_Connection=yes;
    '''
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        cursor.execute("SET SHOWPLAN_XML ON")
        cursor.execute(query)
        
        row = cursor.fetchone()
        if row:
            plan_xml = row[0]

        cursor.execute("SET SHOWPLAN_XML OFF")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error retrieving plan: {e}")

    return plan_xml

@tool
def list_schemas_and_tables() -> str:
    """
    Retrieves a list of available schemas and their tables in the DWH.
    Use this tool to explore the database structure, discover available schemas, and find specific table names before writing queries.
    
    Returns:
        str: A JSON formatted list of dictionaries containing TABLE_SCHEMA, TABLE_NAME, and TABLE_TYPE, or an error message.
    """
    connection_string = f'''
        DRIVER={{ODBC Driver 17 for SQL Server}};
        SERVER={server};
        DATABASE={database};
        Trusted_Connection=yes;
    '''
    query = """
        SELECT 
            TABLE_SCHEMA, 
            TABLE_NAME, 
            TABLE_TYPE 
        FROM 
            INFORMATION_SCHEMA.TABLES 
        ORDER BY 
            TABLE_SCHEMA, 
            TABLE_NAME;
    """
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute(query)
        
        if cursor.description:
            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()
            
            if not rows:
                return json.dumps({
                    "status": "not_found", 
                    "message": "No schemas or tables found in the specified database."
                })
                
            result_data = [dict(zip(columns, row)) for row in rows]
            return json.dumps(result_data, default=str)
        else:
            return json.dumps({"status": "error", "message": "Failed to retrieve schemas and tables metadata."})
            
    except pyodbc.Error as e:
        return json.dumps({"status": "error", "error_message": str(e)})
        
    finally:
        if 'conn' in locals():
            conn.close()

@tool
def knowledge_search(query: str) -> str:
    """
    Search the local knowledge database which has information about the following topics: description of tables in the DWH, connections between tables, structure (data types, PK, FK)).
    Returns top releveant search results.
    Automatically filters out irrelevant noise via reranking.

    Args:
        query (str): Search query or question to look up, e.g. 'Sales.Store' or 'SQL Style Guide'

    Returns:
        str: Most relevant document fragments (Content + Source).
    """
    try:
        results = get_retriever(query)
        if not results:
            return "No documents found for this query. Try rephrasing."
        else:
            return results
    except Exception as e:
        return f"Error searching local knowledge base. Details: {e}."

@tool
def web_search(query: str) -> str:
    """
    Search the web to find up-to-date information.
    Use this FIRST to find relevant URLs and basic summaries. Do not base your final answer solely on these short snippets.",

    Args:
        query (str): The search query or question to look up.

    Returns:
        str: A JSON-formatted string containing list of search results containing 'title', 'url', and 'snippet'.
    """
    processed_results: List[Dict[str, str]] = []

    try:
        raw_results = DDGS().text(query, max_results=max_search_results)
        if not raw_results:
            return processed_results

        for item in raw_results:
            processed_results.append({
                "title": item.get("title", ""),
                "url": item.get("href", ""),
                "snippet": item.get("body", "")
            })

    except Exception as e:
        return f"Error during search for '{query}': {e}"

    return json.dumps(processed_results)

# read_url_pdf will be used at read_url function, not as a separate tool for llm agent
def read_url_pdf(url: str):
    """
    Fetches a PDF from a URL and extracts its text in-memory.
    """
    try:
        # Mute pypdf's warnings about broken pdfs so they don't flood the agent's console
        logging.getLogger("pypdf").setLevel(logging.ERROR)

        response = requests.get(url, timeout=5)
        response.raise_for_status()
        content_type = response.headers.get('Content-Type', '').lower()
        if 'application/pdf' not in content_type:
            return f"Error: The server blocked the download or requires a subscription. It returned an HTML page instead of a PDF (Content-Type: {content_type}).\
                     DO NOT try to read this URL again. Move on and use the other information you have gathered."

        # Load the raw downloaded bytes into a virtual memory file
        pdf_bytes = io.BytesIO(response.content)
        reader = PdfReader(pdf_bytes)

        full_text = []
        for i, page in enumerate(reader.pages):
            page_text = page.extract_text()
            
            if page_text:
                full_text.append(f"--- Page {i + 1} ---\n{page_text}")
            if i > max_search_results:
                break

        final_text = "\n\n".join(full_text)
        
        return final_text

    except Exception as e:
        return f"Error extracting PDF from {url}. Details: {e}. DO NOT try to read this URL again. Move on and use the other information you have gathered."

@tool 
def read_url(url: str) -> str:
    """
    Fetches and extracts the main text content from a given URL.
    Use this AFTER a web search to read the full, in-depth content of a webpage.
    Essential for gathering detailed facts, examples, and deep context for your final report.
    This function acts as a tool for an LLM agent to read the full content of a webpage.
    It deliberately truncates the output to prevent blowing up the LLM's context window
    (context engineering). It also catches errors so the agent can recover.

    Args:
        url (str): The URL of the webpage to read, , e.g. 'https://...'.

    Returns:
        str: The extracted plain text from the webpage, or an error message if extraction fails.
    """

    try:
        if url.endswith('.pdf'):
            text = read_url_pdf(url)

        else: 
            downloaded = trafilatura.fetch_url(url)
            if downloaded is None:
                return f"Error: Unable to fetch content from '{url}'. The page might be inaccessible, invalid, or blocking automated requests."
            text = trafilatura.extract(downloaded)

            if not text:
                return f"Error: Fetched '{url}' successfully, but could not extract meaningful text. The page might rely heavily on JavaScript."

        if len(text) > max_url_content_length:
            text = text[:max_url_content_length]
            return text

        return text

    except Exception as e:
        return f"An unexpected error occurred while reading '{url}': {str(e)}. DO NOT try to read this URL again. Move on and use the other information you have gathered."

tool_registry = {
    "web_search": web_search, 
    "read_url": read_url, 
    "knowledge_search": knowledge_search,
    "execute_sql_query": execute_sql_query,
    "get_table_structure": get_table_structure,
    "ask_user_for_clarification": ask_user_for_clarification,
    "list_schemas_and_tables": list_schemas_and_tables}

tools = [
    web_search, 
    read_url, 
    knowledge_search,
    execute_sql_query,
    get_table_structure,
    ask_user_for_clarification,
    list_schemas_and_tables]