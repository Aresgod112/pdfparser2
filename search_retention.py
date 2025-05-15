"""
Script to extract text from a PDF and search for retention-related information.
"""

from src.pdf_extractor import PDFExtractor

def search_for_terms(text, terms):
    """
    Search for specific terms in the text and print context around them.
    
    Args:
        text (str): The text to search in.
        terms (list): List of terms to search for.
    """
    print(f"Text length: {len(text)}")
    print("\nSearching for retention information...")
    
    found_any = False
    
    for term in terms:
        if term in text.lower():
            found_any = True
            print(f'\nFound "{term}" in the document. Context:')
            
            # Find all occurrences of the term
            term_pos = 0
            while True:
                term_pos = text.lower().find(term, term_pos)
                if term_pos == -1:
                    break
                    
                # Get context around the term
                start = max(0, term_pos - 200)
                end = min(len(text), term_pos + 200)
                context = text[start:end]
                
                # Highlight the term in the context
                term_start_in_context = term_pos - start
                term_end_in_context = term_start_in_context + len(term)
                highlighted_context = (
                    context[:term_start_in_context] + 
                    "**" + context[term_start_in_context:term_end_in_context] + "**" + 
                    context[term_end_in_context:]
                )
                
                print(f"\n{highlighted_context}")
                print("-" * 80)
                
                # Move to next occurrence
                term_pos += len(term)
    
    if not found_any:
        print("No retention-related terms found in the document.")

def main():
    """Main function to extract text and search for retention information."""
    pdf_path = "Pure Healthcare Group - Framework Agreement.pdf"
    
    # Extract text from PDF
    print(f"Extracting text from {pdf_path}...")
    extractor = PDFExtractor()
    text = extractor.extract_text(pdf_path)
    
    # Search for retention-related terms
    retention_terms = [
        'retention', 'retain', 'store', 'storage', 'keep', 'archive', 'preserve',
        'record', 'document', 'data', 'information', 'period', 'duration', 'term'
    ]
    
    search_for_terms(text, retention_terms)

if __name__ == "__main__":
    main()
