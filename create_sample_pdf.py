"""
Script to convert sample_contract.txt to a PDF file.
"""

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER

def text_to_pdf(text_file, pdf_file):
    """
    Convert a text file to a PDF file.
    
    Args:
        text_file (str): Path to the text file.
        pdf_file (str): Path to save the PDF file.
    """
    # Read the text file
    with open(text_file, 'r', encoding='utf-8') as file:
        text = file.read()
    
    # Split the text into lines
    lines = text.split('\n')
    
    # Create a PDF document
    doc = SimpleDocTemplate(
        pdf_file,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # Get styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='Justify',
        alignment=TA_JUSTIFY,
        fontName='Helvetica',
        fontSize=10,
        leading=12
    ))
    styles.add(ParagraphStyle(
        name='Center',
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=14
    ))
    
    # Create content
    content = []
    
    # Process each line
    for line in lines:
        line = line.strip()
        
        # Skip empty lines
        if not line:
            content.append(Spacer(1, 12))
            continue
        
        # Check if it's a heading (all uppercase)
        if line.isupper() and len(line) > 3:
            content.append(Paragraph(line, styles['Center']))
            content.append(Spacer(1, 6))
        else:
            content.append(Paragraph(line, styles['Justify']))
            content.append(Spacer(1, 6))
    
    # Build the PDF
    doc.build(content)
    
    print(f"PDF created successfully: {pdf_file}")

if __name__ == "__main__":
    text_to_pdf('sample_contract.txt', 'sample_contract.pdf')
