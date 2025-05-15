import os
import tempfile
from datetime import datetime

def get_file_name(file_path):
    """
    Extract the file name from a file path.
    
    Args:
        file_path (str): Path to the file.
        
    Returns:
        str: File name without extension.
    """
    return os.path.splitext(os.path.basename(file_path))[0]

def create_temp_file(uploaded_file):
    """
    Create a temporary file from an uploaded file.
    
    Args:
        uploaded_file: Streamlit uploaded file object.
        
    Returns:
        str: Path to the temporary file.
    """
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            # Write the uploaded file to the temporary file
            tmp.write(uploaded_file.getvalue())
            return tmp.name
    except Exception as e:
        print(f"Error creating temporary file: {e}")
        return None

def clean_temp_files(temp_files):
    """
    Clean up temporary files.
    
    Args:
        temp_files (list): List of temporary file paths.
    """
    for file_path in temp_files:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error removing temporary file {file_path}: {e}")

def generate_output_filename(prefix="contract_data"):
    """
    Generate a filename for the output CSV file.
    
    Args:
        prefix (str): Prefix for the filename.
        
    Returns:
        str: Generated filename.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.csv"

def format_extraction_results(results):
    """
    Format extraction results for display.
    
    Args:
        results (list): List of dictionaries containing extraction results.
        
    Returns:
        list: Formatted results for display.
    """
    formatted_results = []
    
    for i, result in enumerate(results):
        # Only include the fields specified by the user: File, Effective Date, Start Date, Initial Term, Further Term
        formatted_result = {
            "File": result.get("file_name", f"Document {i+1}"),
            "Effective Date": result.get("effective_date", "Not found"),
            "Start Date": result.get("start_date", "Not found"),
            "Initial Term": result.get("initial_term", "Not found"),
            "Further Term": result.get("further_term", "Not found")
        }
            
        formatted_results.append(formatted_result)
        
    return formatted_results

def handle_missing_fields(results):
    """
    Handle missing fields in extraction results.
    
    Args:
        results (list): List of dictionaries containing extraction results.
        
    Returns:
        tuple: (results with missing fields handled, count of missing fields)
    """
    missing_count = 0
    
    for result in results:
        # Only count missing fields for the ones we're displaying
        for field in ['effective_date', 'start_date', 'initial_term', 'further_term']:
            if not result.get(field):
                result[field] = "Not found"
                missing_count += 1
                
    return results, missing_count
