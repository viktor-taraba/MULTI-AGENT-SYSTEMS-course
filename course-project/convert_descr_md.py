from docx import Document

def local_docx_to_markdown(input_filepath, output_filepath=None):
    try:
        doc = Document(input_filepath)
    except Exception as e:
        return f"Error loading document: {e}"
    
    md = []
    
    # 2. Extract the title and description from paragraphs
    title = doc.paragraphs[0].text.strip() if doc.paragraphs else "Table Documentation"
    md.append(f"# {title}\n")
    
    for p in doc.paragraphs[1:]:
        text = p.text.strip()
        if text and text not in ["Columns", "Relations", "Unique keys", "Used by", "Triggers"]:
            md.append(f"> {text}\n")
            break
            
    for table in doc.tables:
        if not table.rows:
            continue
            
        # Read the first row to figure out what kind of table this is
        header_cells = [cell.text.strip() for cell in table.rows[0].cells]
        header_text = " ".join(header_cells).lower()
        
        # -- METADATA TABLE (Schema, Module, etc.) --
        if "documentation" in header_text or "schema" in header_text:
            for row in table.rows:
                cells = [cell.text.strip() for cell in row.cells]
                # Avoid printing empty rows
                if len(cells) >= 2 and cells[0]:
                    md.append(f"**{cells[0]}:** {cells[1]}")
            md.append("\n---")
            
        # -- STANDARD DATA TABLES (Columns, Relations, Keys) --
        elif any(keyword in header_text for keyword in ["data type", "primary table", "join", "key name"]):
            
            if "data type" in header_text:
                md.append("\n## Columns")
            elif "join" in header_text:
                md.append("\n## Relations")
            elif "key name" in header_text:
                md.append("\n## Unique Keys")

            md.append("| " + " | ".join(header_cells) + " |")
            md.append("|" + "|".join(["---"] * len(header_cells)) + "|")
            
            for row in table.rows[1:]:
                # Replace newlines inside cells so Markdown tables don't break
                cells = [cell.text.strip().replace('\n', ' ') for cell in row.cells]
                # Replace empty cells with a dash for cleaner Markdown
                cells = [c if c else "-" for c in cells]
                md.append("| " + " | ".join(cells) + " |")

    final_md = "\n".join(md)
    
    if output_filepath:
        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write(final_md)
        print(f"Successfully saved to {output_filepath}")
        
    return final_md

url = "C:\\Users\\Viktor\\OneDrive\\Desktop\\HumanResources.EmployeeDepartmentHistory.docx"#dbo.AWBuildVersion.docx"#HumanResources.docx"
markdown_output = local_docx_to_markdown(url)
print(markdown_output)