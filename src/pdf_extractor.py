import os
import PyPDF2
import pytesseract
import pdfplumber
from PIL import Image
import io
import tempfile

class PDFExtractor:
    """
    Class for extracting text from PDF files.
    Handles both text-based PDFs and scanned/image-based PDFs.
    """
    
    def __init__(self, ocr_language='eng'):
        """
        Initialize the PDF extractor.
        
        Args:
            ocr_language (str): Language for OCR. Default is 'eng' (English).
        """
        self.ocr_language = ocr_language
        
    def extract_text(self, pdf_file):
        """
        Extract text from a PDF file.
        
        Args:
            pdf_file: File object or path to the PDF file.
            
        Returns:
            str: Extracted text from the PDF.
        """
        # First try standard text extraction
        text = self._extract_text_standard(pdf_file)
        
        # If little or no text was extracted, try OCR
        if not text or len(text.strip()) < 100:  # Arbitrary threshold
            text = self._extract_text_ocr(pdf_file)
            
        return text
    
    def _extract_text_standard(self, pdf_file):
        """
        Extract text from a PDF using standard methods (no OCR).
        
        Args:
            pdf_file: File object or path to the PDF file.
            
        Returns:
            str: Extracted text from the PDF.
        """
        try:
            # Try with pdfplumber first (often better for maintaining layout)
            with pdfplumber.open(pdf_file) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() or ""
                    
            # If pdfplumber didn't extract much, try PyPDF2
            if not text or len(text.strip()) < 50:
                if isinstance(pdf_file, str):
                    with open(pdf_file, 'rb') as file:
                        reader = PyPDF2.PdfReader(file)
                        text = ""
                        for page in reader.pages:
                            text += page.extract_text() or ""
                else:
                    # Reset file pointer if it's a file object
                    pdf_file.seek(0)
                    reader = PyPDF2.PdfReader(pdf_file)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text() or ""
                        
            return text
        except Exception as e:
            print(f"Error in standard text extraction: {e}")
            return ""
    
    def _extract_text_ocr(self, pdf_file):
        """
        Extract text from a PDF using OCR.
        
        Args:
            pdf_file: File object or path to the PDF file.
            
        Returns:
            str: Extracted text from the PDF.
        """
        try:
            from pdf2image import convert_from_path, convert_from_bytes
            
            text = ""
            
            # Convert PDF to images
            if isinstance(pdf_file, str):
                images = convert_from_path(pdf_file)
            else:
                # Reset file pointer if it's a file object
                pdf_file.seek(0)
                pdf_bytes = pdf_file.read()
                images = convert_from_bytes(pdf_bytes)
            
            # Process each page
            for image in images:
                # Use pytesseract to extract text from the image
                page_text = pytesseract.image_to_string(image, lang=self.ocr_language)
                text += page_text + "\n\n"
                
            return text
        except Exception as e:
            print(f"Error in OCR text extraction: {e}")
            return ""
