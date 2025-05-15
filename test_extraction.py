"""
Test script for field extraction from the sample contract text.
This script demonstrates how the field extraction works without needing a PDF file.
"""

from src.field_extractor import FieldExtractor

def main():
    """Main function to test field extraction."""
    
    print("Testing field extraction on sample contract text...")
    
    try:
        # Read the sample contract text
        with open('sample_contract.txt', 'r', encoding='utf-8') as file:
            text = file.read()
        
        # Initialize field extractor
        field_extractor = FieldExtractor()
        
        # Extract fields from text
        print("Extracting fields...")
        fields = field_extractor.extract_fields(text)
        
        # Print results
        print("\nExtraction Results:")
        print("-" * 50)
        
        # Expected values from our sample contract
        expected = {
            'client_name': 'GLOBEX INDUSTRIES',
            'contract_start_date': '2025-01-15',  # January 15, 2025 (Effective Date)
            'sign_date': '2025-01-15',  # January 15, 2025 (signature date)
            'initial_term': '24 months',
            'further_term': 'automatically renew for successive 12-month periods'
        }
        
        # Compare extracted values with expected values
        for field, value in fields.items():
            expected_value = expected.get(field, 'N/A')
            extracted_value = value or 'Not found'
            
            print(f"{field.replace('_', ' ').title()}:")
            print(f"  Expected: {expected_value}")
            print(f"  Extracted: {extracted_value}")
            
            if expected_value != 'N/A':
                if extracted_value == expected_value:
                    print(f"  ✅ Match")
                elif extracted_value != 'Not found' and expected_value in extracted_value:
                    print(f"  ⚠️ Partial match")
                else:
                    print(f"  ❌ No match")
            print()
        
    except Exception as e:
        print(f"Error during extraction test: {str(e)}")

if __name__ == "__main__":
    main()
