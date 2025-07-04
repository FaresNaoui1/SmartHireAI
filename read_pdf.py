from PyPDF2 import PdfReader

def read_pdf(pdf_path):
     pdf = PdfReader(pdf_path)
     print(pdf.metadata)
     for page in pdf.pages:
       print(page.extract_text())
       contex= page.extract_text()
     return contex
# Function to read PDF files and extract text
def read_pdfs(pdfs):

    contexts = []
    for pdf_path in pdfs:
        reader = PdfReader(pdf_path)
        text_chunks = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_chunks.append(text)
        
        full_text = "\n".join(text_chunks)
        contexts.append(full_text)
    return contexts
