from fastapi import FastAPI, UploadFile, File, HTTPException
from pypdf import PdfReader
from io import BytesIO
from app.document import chunk_text
from app.retrieval import find_relevant_chunks
from app.LLM import generate_answer

app = FastAPI()

documents = {}

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

    documents[file.filename] = chunks

    return {
        "filename": file.filename,
        "text": text,
        "chunks": chunks,
        "chunk_count": len(chunks)
    }

@app.get("/ask")
def ask_question(filename: str, question: str):
    if filename not in documents:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    relevant_chunks = find_relevant_chunks(
        question,
        documents[filename]
    )

    if not relevant_chunks:
        raise HTTPException(
            status_code=404,
            detail="No relevant information found in the document"
        )

    sources = [
        {
            "source_id": index + 1,
            "text": chunk
        }
        for index, chunk in enumerate(relevant_chunks)
    ]

    context = "\n\n".join(
        f"[Source {source['source_id']}]\n{source['text']}"
        for source in sources
    )

    answer = generate_answer(question, context)

    return {
    "filename": filename,
    "question": question,
    "answer": answer,
    "sources": sources
    }