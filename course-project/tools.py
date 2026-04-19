import os

def get_model_and_relationships(dataset_path: str) -> str:
    """
    Reads and returns the raw text content of model.tmdl and relationships.tmdl.
    Use this tool to understand the overall dataset configuration and table relationships.
    
    Args:
        dataset_path (str): The root directory of the .pbip dataset.
    """
    result = []
    
    model_path = os.path.join(dataset_path, "model.tmdl")
    if os.path.exists(model_path):
        with open(model_path, "r", encoding="utf-8") as f:
            result.append(f"--- model.tmdl ---\n{f.read()}")
    else:
        result.append("--- model.tmdl ---\n(File not found)")

    rel_path = os.path.join(dataset_path, "relationships.tmdl")
    if os.path.exists(rel_path):
        with open(rel_path, "r", encoding="utf-8") as f:
            result.append(f"--- relationships.tmdl ---\n{f.read()}")
    else:
        result.append("--- relationships.tmdl ---\n(File not found - relationships may be defined within individual table files)")

    return "\n\n".join(result)

def get_table_content(dataset_path: str, table_name: str = None) -> str:
    """
    Returns the raw TMDL content for a specific table. 
    Automatically excludes the 'source' block (Power Query M code) to save LLM context window space, 
    as it is not needed for DAX measure creation.
    
    If no table_name is provided, it returns a list of all available tables in the dataset.
    
    Args:
        dataset_path (str): The root directory of the .pbip dataset.
        table_name (str, optional): The exact name of the table to read (e.g., 'Sales').
    """
    tables_dir = os.path.join(dataset_path, "tables")
    
    if not os.path.exists(tables_dir):
        return f"Error: The 'tables' directory was not found at {tables_dir}."

    if not table_name:
        try:
            tables = [f.replace(".tmdl", "") for f in os.listdir(tables_dir) if f.endswith(".tmdl")]
            return "Available tables:\n- " + "\n- ".join(tables)
        except Exception as e:
            return f"Error reading tables directory: {str(e)}"
    
    safe_table_name = "".join([c for c in table_name if c.isalpha() or c.isdigit() or c in (' ', '_', '-')]).strip()
    table_path = os.path.join(tables_dir, f"{safe_table_name}.tmdl")
    
    if os.path.exists(table_path):
        try:
            with open(table_path, "r", encoding="utf-8-sig") as f:
                lines = f.readlines()
            
            filtered_lines = []
            in_source_block = False
            source_indent_level = 0
            
            for line in lines:
                stripped = line.lstrip()
                
                if not stripped:
                    if not in_source_block:
                        filtered_lines.append(line)
                    continue
                    
                current_indent = len(line) - len(stripped)
                
                # If we are currently skipping a source block...
                if in_source_block:
                    # If the line is indented further than the 'source' declaration, it belongs to the M code
                    if current_indent > source_indent_level:
                        continue 
                    # If the indentation drops back down, the source block is over
                    else:
                        in_source_block = False
                
                # Check if we are entering a new source block
                if stripped.startswith("source =") or stripped.startswith("source:"):
                    in_source_block = True
                    source_indent_level = current_indent
                    
                    indent_spaces = " " * current_indent
                    filtered_lines.append(f"{indent_spaces}source = (Power Query M code excluded for token efficiency)\n")
                    continue
                    
                if not in_source_block:
                    filtered_lines.append(line)
                    
            return f"--- {safe_table_name}.tmdl ---\n" + "".join(filtered_lines)
            
        except Exception as e:
            return f"Error reading table '{safe_table_name}': {str(e)}"
    else:
        return f"Error: Table file '{safe_table_name}.tmdl' not found. Please check the available tables."



print(get_table_content("C:\\Users\\Viktor\\source\\repos\\MULTI-AGENT-SYSTEMS-course\\course-project\\reports\\Corporate Spend\\Corporate Spend.SemanticModel\\definition"))
print(get_table_content("C:\\Users\\Viktor\\source\\repos\\MULTI-AGENT-SYSTEMS-course\\course-project\\reports\\Corporate Spend\\Corporate Spend.SemanticModel\\definition","Department"))

поки план мінімум - хай розкаже про що звіт та додасть документацію мір

# print(get_model_and_relationships("C:\\Users\\Viktor\\source\\repos\\MULTI-AGENT-SYSTEMS-course\\course-project\\reports\\Corporate Spend\\Corporate Spend.SemanticModel\\definition"))