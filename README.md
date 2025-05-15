# Contract PDF Parser

A Python application that extracts key information from contract PDFs using text extraction and OCR techniques.

## 🔍 Features

- **Upload Multiple PDFs**: Process one or multiple contract PDFs at once
- **Smart Text Extraction**: 
  - Uses standard PDF libraries for text-based PDFs
  - Automatically falls back to OCR for scanned/image-based PDFs
- **Field Extraction**: Extracts the following fields from contracts:
  - Effective Date
  - Start Date
  - Initial Term
  - Further Term
- **Enhanced Results Display**: 
  - Shows extracted data in a well-formatted tabular format
  - Highlights missing fields in red for easy identification
  - Provides summary statistics (files processed, fields extracted, success rate)
  - Includes filtering options to focus on specific files or missing fields
- **Export Options**: 
  - Download results as a CSV file
  - Export to Excel with formatted headers and auto-sized columns
- **Error Handling**: Provides feedback for missing or unrecognized fields
- **Multi-language OCR**: Supports English, French, German, Spanish, and Italian

## 📋 Requirements

- Python 3.8+
- Tesseract OCR (for processing scanned PDFs)
- Required Python packages (see `requirements.txt`)

## 🚀 Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/contract-pdf-parser.git
   cd contract-pdf-parser
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Install Tesseract OCR:
   - **Windows**: Download and install from [here](https://github.com/UB-Mannheim/tesseract/wiki)
   - **macOS**: `brew install tesseract`
   - **Linux**: `sudo apt install tesseract-ocr`

## 🖥️ Usage

1. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

2. Open your web browser and navigate to the URL displayed in the terminal (typically http://localhost:8501)

3. Upload one or more PDF files containing contracts

4. Click "Process Files" to extract information

5. View the results in the table and download as CSV if needed

## 📝 How It Works

1. **PDF Text Extraction**:
   - First attempts to extract text using standard PDF libraries (pdfplumber and PyPDF2)
   - If little or no text is extracted, falls back to OCR using Tesseract

2. **Field Extraction**:
   - Uses regex patterns and keyword-based extraction to identify specific fields
   - Applies multiple patterns for each field to increase accuracy
   - Formats dates into a standard format when possible

3. **Results Handling**:
   - Displays all extracted fields in a table
   - Marks missing fields as "Not found"
   - Provides export functionality to save results

## 🧠 Advanced Features

- **Session State**: Remembers previously processed files
- **Progress Tracking**: Shows progress during processing
- **Temporary File Management**: Automatically cleans up temporary files
- **Multi-language Support**: Select the appropriate language for OCR processing

## 📄 Project Structure

- `app.py`: Main Streamlit application
- `src/pdf_extractor.py`: PDF text extraction module
- `src/field_extractor.py`: Field extraction using regex and keywords
- `src/utils/export.py`: CSV export functionality
- `src/utils/helpers.py`: Helper functions

## 🔧 Customization

- **Adding New Fields**: Extend the patterns in `field_extractor.py`
- **Improving Extraction**: Add more regex patterns for existing fields
- **UI Customization**: Modify the Streamlit UI in `app.py`

## 📚 License

This project is licensed under the MIT License - see the LICENSE file for details.
