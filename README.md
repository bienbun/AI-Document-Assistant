# AI Document Assistant

An AI-powered document question-answering application built with Python, FastAPI, and the Gemini API.

The goal of this project is to allow users to upload documents and ask questions about their contents. The application processes uploaded documents, retrieves relevant information, and provides that context to a large language model to generate more grounded answers.

## Features

- Upload and process user documents
- Ask questions about uploaded document content
- Retrieve relevant document context for each question
- Generate AI-assisted responses using the Gemini API
- FastAPI backend for handling document and question requests

## Tech Stack

- Python
- FastAPI
- Google Gemini API

## How It Works

1. A user uploads a document.
2. The application extracts and processes the document content.
3. The content is prepared for retrieval.
4. When the user asks a question, relevant document information is retrieved.
5. The retrieved context is provided to Gemini.
6. Gemini generates an answer based on the document context.

## Project Status

Currently in development.

I am currently working on the document ingestion and retrieval pipeline and expanding the system to provide more accurate context-aware answers.

## Future Improvements

- Support additional document formats
- Improve document chunking and retrieval
- Add persistent document storage
- Add conversation history
- Improve error handling
- Add document management
- Deploy the application
