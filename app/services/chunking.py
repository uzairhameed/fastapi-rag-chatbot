from io import BytesIO
from pypdf import PdfReader
from app.config import CHUNK_SIZE, CHUNK_OVERLAP


# Extract text from a TXT or PDF file.

def extract_text(file_bytes: bytes, filename: str)->str:
    
    if filename.lower().endswith(".txt"):
        text = file_bytes.decode("utf-8")

    elif filename.lower().endswith(".pdf"):
        pdf = PdfReader(BytesIO(file_bytes))
        

        text = "\n".join(
            page.extract_text() or ""
            for page in pdf.pages
        )

    else:
        raise ValueError("Unsupported file format.Upload TXT or PDF.")

    if not text.strip():
        raise ValueError("Unsupported file format.Upload TXT or PDF.")

    return text

# Split text into overlapping chunks.
def chunk_text(text: str)-> list[str]:
    chunks =[]
    start=0

    while start < len(text):
        end =start + CHUNK_SIZE

        chunk= text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks
