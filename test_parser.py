"""
Test script for the Contract PDF Parser.
This script demonstrates how to use the parser programmatically without the Streamlit interface.
"""

import os
import sys
import pandas as pd
from src.pdf_extractor import PDFExtractor
from src.field_extractor import FieldExtractor
from src.utils.export import export_to_csv

def main():
    """Main function to test the PDF parser."""
    
    # Check if a PDF file path was provided
    if len(sys.argv) < 2:
        print("Usage: python test_parser.py <path_to_pdf_file>")
        return
    
    # Get the PDF file path from command line arguments
    pdf_path = sys.argv[1]
    
    # Check if the file exists
    if not os.path.exists(pdf_path):
        print(f"Error: File '{pdf_path}' not found.")
        return
    
    # Check if the file is a PDF
    if not pdf_path.lower().endswith('.pdf'):
        print(f"Error: File '{pdf_path}' is not a PDF.")
        return
    
    print(f"Processing '{pdf_path}'...")
    
    try:
        # Initialize extractors
        pdf_extractor = PDFExtractor(ocr_language='eng')
        field_extractor = FieldExtractor()
        
        # Extract text from PDF
        print("Extracting text...")
        text = pdf_extractor.extract_text(pdf_path)
        
        if not text or len(text.strip()) < 10:
            print("Warning: Little or no text extracted. The file may be corrupted or heavily image-based.")
            return
        
        # Extract fields from text
        print("Extracting fields...")
        fields = field_extractor.extract_fields(text)
        
        # Add file name to results
        fields['file_name'] = os.path.basename(pdf_path)
        
        # Print results
        print("\nExtraction Results:")
        print("-" * 50)
        for field, value in fields.items():
            print(f"{field.replace('_', ' ').title()}: {value or 'Not found'}")
        
        # Export to CSV (optional)
        if len(sys.argv) > 2 and sys.argv[2].lower() == '--export':
            output_path = os.path.splitext(pdf_path)[0] + "_extracted.csv"
            export_to_csv([fields], output_path)
            print(f"\nResults exported to '{output_path}'")
        
    except Exception as e:
        print(f"Error processing file: {str(e)}")

if __name__ == "__main__":
    main()
