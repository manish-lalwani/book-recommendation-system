import pdfplumber

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extracts text from the uploaded PDF file.
    """
    with pdfplumber.open(file_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text
