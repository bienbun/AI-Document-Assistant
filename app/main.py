from fastapi import FastAPI, UploadFile, File, HTTPException
from pypdf import PdfReader
from io import BytesIO

from app.document import chunk_text
from app.retrieval import find_relevant_chunks
from app.LLM import generate_answer
from app.storage import load_documents, save_documents


app = FastAPI()

# Load previously saved documents when the server starts
documents = load_documents()


@app.get("/")
def home():
    return {"message": "AI Document Assistant is running"}


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )

    contents = await file.read()
    pdf = PdfReader(BytesIO(contents))

    text = ""

    for page in pdf.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    chunks = chunk_text(text)

    # Save this document's chunks in memory
    documents[file.filename] = chunks

    # Save all documents to persistent JSON storage
    save_documents(documents)

    return {
        "filename": file.filename,
        "text": text,
        "chunks": chunks,
        "chunk_count": len(chunks)
    }


@app.get("/documents")
def list_documents():
    return {
        "documents": list(documents.keys()),
        "count": len(documents)
    }


@app.delete("/documents/{filename}")
def delete_document(filename: str):
    if filename not in documents:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    del documents[filename]

    # Update persistent storage after deletion
    save_documents(documents)

    return {
        "message": "Document deleted successfully",
        "filename": filename
    }


@app.get("/ask")
def ask_question(filename: str, question: str):
    # Check that the requested document exists
    if filename not in documents:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    # Get chunks belonging to the selected document
    document_chunks = documents[filename]

    # Retrieve the most relevant chunks
    relevant_chunks = find_relevant_chunks(
        question,
        document_chunks
    )

    if not relevant_chunks:
        raise HTTPException(
            status_code=404,
            detail="No relevant information found in the document"
        )

    # Give each retrieved chunk a source ID
    sources = [
        {
            "source_id": index + 1,
            "text": chunk
        }
        for index, chunk in enumerate(relevant_chunks)
    ]

    # Build context for Gemini with source labels
    context = "\n\n".join(
        f"[Source {source['source_id']}]\n{source['text']}"
        for source in sources
    )

    # Generate grounded answer
    answer = generate_answer(
        question,
        context
    )

    return {
        "filename": filename,
        "question": question,
        "answer": answer,
        "sources": sources
    }