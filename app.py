import os
import sys
import traceback
import streamlit as st
import pandas as pd
import base64
from io import BytesIO

# Add basic logging
print("Starting PDF Parser application...")
print(f"Python version: {sys.version}")
print(f"Current working directory: {os.getcwd()}")

try:
    from src.pdf_extractor import PDFExtractor
    from src.field_extractor import FieldExtractor
    from src.utils.export import export_to_csv
    from src.utils.helpers import (
        create_temp_file, 
        clean_temp_files, 
        get_file_name, 
        generate_output_filename,
        format_extraction_results,
        handle_missing_fields
    )
    print("Successfully imported all modules")
except Exception as e:
    print(f"Error importing modules: {e}")
    traceback.print_exc()
    sys.exit(1)

try:
    # Set page configuration
    print("Setting up Streamlit page configuration...")
    st.set_page_config(
        page_title="Contract PDF Parser",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    print("Page configuration set successfully")
except Exception as e:
    print(f"Error setting page configuration: {e}")
    traceback.print_exc()

try:
    # Initialize session state variables if they don't exist
    print("Initializing session state variables...")
    if 'extraction_results' not in st.session_state:
        # Add sample data for testing
        st.session_state.extraction_results = [
            {
                'print_name': 'John Smith',
                'title': 'CEO',
                'effective_date': '2023-01-01',
                'start_date': '2023-01-15',
                'initial_term': '12 months',
                'further_term': 'Automatically renews for 12 months',
                'file_name': 'sample_contract.pdf'
            },
            {
                'print_name': 'Jane Doe',
                'title': 'CTO',
                'effective_date': '2023-02-01',
                'start_date': None,
                'initial_term': '24 months',
                'further_term': None,
                'file_name': 'sample_contract_2.pdf'
            }
        ]
    if 'temp_files' not in st.session_state:
        st.session_state.temp_files = []
    if 'processed_files' not in st.session_state:
        st.session_state.processed_files = set(['sample_contract.pdf', 'sample_contract_2.pdf'])
    print("Session state variables initialized successfully")
except Exception as e:
    print(f"Error initializing session state: {e}")
    traceback.print_exc()

def main():
    """Main function to run the Streamlit app."""
    print("Entering main function...")
    
    # Add custom CSS
    st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            color: #1E88E5;
            margin-bottom: 1rem;
        }
        .sub-header {
            font-size: 1.5rem;
            color: #424242;
            margin-bottom: 1rem;
        }
        .success-text {
            color: #4CAF50;
            font-weight: bold;
        }
        .warning-text {
            color: #FFC107;
            font-weight: bold;
        }
        .error-text {
            color: #F44336;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<p class="main-header">📄 Contract PDF Parser</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Extract key information from contract PDFs</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("Settings")
        
        # OCR language selection
        ocr_language = st.selectbox(
            "OCR Language",
            options=["eng", "fra", "deu", "spa", "ita"],
            index=0,
            help="Select the language for OCR processing of scanned PDFs."
        )
        
        # Clear results button
        if st.button("Clear All Results"):
            # Clean up temporary files
            clean_temp_files(st.session_state.temp_files)
            
            # Reset session state
            st.session_state.extraction_results = []
            st.session_state.temp_files = []
            st.session_state.processed_files = set()
            
            st.success("All results cleared!")
            
        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        This application extracts key information from contract PDFs:
        - Effective Date
        - Start Date
        - Initial Term
        - Further Term
        
        It supports both text-based PDFs and scanned documents (using OCR).
        """)
    
    # Main content
    # File uploader
    uploaded_files = st.file_uploader(
        "Upload contract PDF files",
        type=["pdf"],
        accept_multiple_files=True,
        help="Upload one or more PDF files containing contract information."
    )
    
    # Process button
    col1, col2 = st.columns([1, 5])
    with col1:
        process_button = st.button("Process Files", type="primary", use_container_width=True)
    
    # Process files when button is clicked
    if process_button and uploaded_files:
        with st.spinner("Processing PDF files..."):
            process_files(uploaded_files, ocr_language)
    
    # Display results if available
    if st.session_state.extraction_results:
        display_results()
    else:
        st.info("No files have been processed yet. Upload and process PDF files to see extraction results.")
    
    # Footer
    st.markdown("---")
    st.markdown("Developed with ❤️ using Streamlit, PyPDF2, and Tesseract OCR")

def process_files(uploaded_files, ocr_language):
    """
    Process uploaded PDF files.
    
    Args:
        uploaded_files (list): List of uploaded PDF files.
        ocr_language (str): Language for OCR processing.
    """
    # Initialize extractors
    pdf_extractor = PDFExtractor(ocr_language=ocr_language)
    field_extractor = FieldExtractor()
    
    # Track new results
    new_results = []
    new_temp_files = []
    
    # Process each file
    progress_bar = st.progress(0)
    
    for i, uploaded_file in enumerate(uploaded_files):
        # Skip if already processed
        if uploaded_file.name in st.session_state.processed_files:
            continue
        
        try:
            # Update progress
            progress_percent = (i + 1) / len(uploaded_files)
            progress_bar.progress(progress_percent)
            
            # Create a temporary file
            temp_file_path = create_temp_file(uploaded_file)
            if not temp_file_path:
                st.error(f"Failed to process {uploaded_file.name}. Could not create temporary file.")
                continue
                
            new_temp_files.append(temp_file_path)
            
            # Extract text from PDF
            text = pdf_extractor.extract_text(temp_file_path)
            
            if not text or len(text.strip()) < 10:  # Arbitrary threshold
                st.warning(f"Little or no text extracted from {uploaded_file.name}. The file may be corrupted or heavily image-based.")
                continue
            
            # Extract fields from text
            fields = field_extractor.extract_fields(text)
            
            # Add file name to results
            fields['file_name'] = uploaded_file.name
            
            # Add to results
            new_results.append(fields)
            
            # Mark as processed
            st.session_state.processed_files.add(uploaded_file.name)
            
        except Exception as e:
            st.error(f"Error processing {uploaded_file.name}: {str(e)}")
    
    # Clear progress bar
    progress_bar.empty()
    
    # Update session state
    st.session_state.extraction_results.extend(new_results)
    st.session_state.temp_files.extend(new_temp_files)
    
    # Show success message
    if new_results:
        st.success(f"Successfully processed {len(new_results)} new file(s)!")
    else:
        st.info("No new files to process.")

def display_results():
    """Display extraction results in a tabular format with improved formatting."""
    
    # Handle missing fields
    results, missing_count = handle_missing_fields(st.session_state.extraction_results)
    
    # Format results for display
    formatted_results = format_extraction_results(results)
    
    # Convert to DataFrame for display
    df = pd.DataFrame(formatted_results)
    
    # Display results section header
    st.markdown('<p class="sub-header">Extraction Results</p>', unsafe_allow_html=True)
    
    # Add summary statistics
    total_files = len(formatted_results)
    total_fields = total_files * 4  # 4 main fields per file (Effective Date, Start Date, Initial Term, Further Term)
    success_rate = ((total_fields - missing_count) / total_fields) * 100 if total_fields > 0 else 0
    
    # Create metrics row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Files Processed", f"{total_files}")
    with col2:
        st.metric("Fields Extracted", f"{total_fields - missing_count}/{total_fields}")
    with col3:
        st.metric("Success Rate", f"{success_rate:.1f}%")
    
    # Show warning if missing fields with more details
    if missing_count > 0:
        st.warning(
            f"{missing_count} fields could not be extracted. They are marked as 'Not found' in the table below. "
            "This may be due to non-standard formatting in the original documents."
        )
    
    # Add filter options
    st.markdown("### Filter Results")
    filter_cols = st.columns(3)
    
    # File filter
    with filter_cols[0]:
        if len(df) > 0 and 'File' in df.columns:
            selected_files = st.multiselect(
                "Filter by File",
                options=df['File'].unique(),
                default=[]
            )
    
    # Field filter
    with filter_cols[1]:
        show_missing = st.checkbox("Show Missing Fields Only", value=False)
    
    # Apply filters
    filtered_df = df.copy()
    if len(df) > 0:
        if selected_files:
            filtered_df = filtered_df[filtered_df['File'].isin(selected_files)]
        
        if show_missing:
            # Create a mask for rows with at least one "Not found" value
            mask = filtered_df.apply(lambda row: any(str(val) == "Not found" for val in row), axis=1)
            filtered_df = filtered_df[mask]
            
    # Add a message if no results after filtering
    if len(filtered_df) == 0 and len(df) > 0:
        st.info("No results match the current filter criteria. Try adjusting your filters.")
    elif len(df) == 0:
        st.info("No files have been processed yet. Upload and process PDF files to see results here.")
    
    # Style the dataframe
    def highlight_missing(val):
        if val == "Not found":
            return 'color: #F44336; font-weight: bold'
        return ''
    
    # Apply styling (using .map instead of .applymap which is deprecated)
    styled_df = filtered_df.style.map(highlight_missing)
    
    # Display table with improved styling
    st.markdown("### Extracted Data")
    st.dataframe(
        styled_df,
        use_container_width=True,
        height=400,  # Fixed height with scrolling
    )
    
    # Export options with better styling
    st.markdown("### Export Options")
    export_cols = st.columns([1, 1, 3])
    
    with export_cols[0]:
        # Generate CSV download link with better styling
        csv_filename = generate_output_filename()
        csv = filtered_df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        
        download_button_style = """
            <style>
            .download-button {
                background-color: #4CAF50;
                color: white;
                padding: 10px 15px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 5px;
            }
            </style>
        """
        
        st.markdown(download_button_style, unsafe_allow_html=True)
        href = f'<a href="data:file/csv;base64,{b64}" download="{csv_filename}" class="download-button">Download CSV</a>'
        st.markdown(href, unsafe_allow_html=True)
    
    with export_cols[1]:
        # Generate Excel download option
        if st.button("Download Excel", type="primary"):
            # Create a BytesIO object
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                filtered_df.to_excel(writer, sheet_name='Extraction Results', index=False)
                
                # Get the xlsxwriter workbook and worksheet objects
                workbook = writer.book
                worksheet = writer.sheets['Extraction Results']
                
                # Add some formatting
                header_format = workbook.add_format({
                    'bold': True,
                    'bg_color': '#D3D3D3',
                    'border': 1
                })
                
                # Write the column headers with the defined format
                for col_num, value in enumerate(filtered_df.columns.values):
                    worksheet.write(0, col_num, value, header_format)
                    
                # Set column widths
                for i, col in enumerate(filtered_df.columns):
                    max_len = max(
                        filtered_df[col].astype(str).map(len).max(),
                        len(col)
                    ) + 2
                    worksheet.set_column(i, i, max_len)
            
            # Set up download link
            b64_excel = base64.b64encode(output.getvalue()).decode()
            excel_filename = generate_output_filename().replace('.csv', '.xlsx')
            href_excel = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64_excel}" download="{excel_filename}">Click to Download</a>'
            st.markdown(href_excel, unsafe_allow_html=True)

if __name__ == "__main__":
    try:
        print("Starting main function...")
        main()
        print("Main function completed successfully")
    except Exception as e:
        print(f"Error in main function: {e}")
        traceback.print_exc()
        st.error(f"An error occurred: {str(e)}")
