import os
import csv
import pandas as pd

def export_to_csv(data, output_path):
    """
    Export extracted data to a CSV file.
    
    Args:
        data (list): List of dictionaries containing the extracted fields.
        output_path (str): Path to save the CSV file.
        
    Returns:
        bool: True if export was successful, False otherwise.
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Convert to DataFrame for easier handling
        df = pd.DataFrame(data)
        
        # Write to CSV
        df.to_csv(output_path, index=False)
        
        return True
    except Exception as e:
        print(f"Error exporting to CSV: {e}")
        return False

def export_to_csv_basic(data, output_path):
    """
    Export extracted data to a CSV file using the csv module.
    Fallback method if pandas is not available.
    
    Args:
        data (list): List of dictionaries containing the extracted fields.
        output_path (str): Path to save the CSV file.
        
    Returns:
        bool: True if export was successful, False otherwise.
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Get field names from the first dictionary
        if data and len(data) > 0:
            fieldnames = list(data[0].keys())
        else:
            fieldnames = ['client_name', 'contract_start_date', 'sign_date', 'initial_term', 'further_term']
        
        # Write to CSV
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
        
        return True
    except Exception as e:
        print(f"Error exporting to CSV (basic): {e}")
        return False
