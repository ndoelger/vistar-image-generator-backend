from pypdf import PdfReader

def extract_text_from_pdf(file_stream):
    reader = PdfReader(file_stream)
    return "\n".join(page.extract_text() or "" for page in reader.pages)
