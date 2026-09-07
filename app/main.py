from fastapi import FastAPI, UploadFile, File, HTTPException
from pypdf import PdfReader
from io import BytesIO
from app.document import chunk_text
from app.retrieval import find_relevant_chunks

app = FastAPI()

document_chunks = []

@app.get("/")
def home():
    return {"message": "AI Document Assistant is running"}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    contents = await file.read()
    pdf = PdfReader(BytesIO(contents))

    text = ""

    for page in pdf.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    chunks = chunk_text(text)

    global document_chunks
    document_chunks = chunks

    return {
        "filename": file.filename,
        "text": text,
        "chunks": chunks,
        "chunk_count": len(chunks)
    }

@app.get("/ask")
def ask_question(question: str):
    relevant_chunks = find_relevant_chunks(question, document_chunks)

    return {
        "question": question,
        "relevant_chunks": relevant_chunks
    }