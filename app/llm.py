def generate_answer(question: str, context: str) -> str:
    prompt = f"""
    Answer the user's question using only the document context below.

    You may make reasonable inferences from the context, but do not use
    information that is not supported by the document.

    When you use information from a source, cite it using the source label
    exactly as written, for example [Source 1] or [Source 2].

    Context:
    {context}

    Question:
    {question}

    If the context does not contain enough information to answer the question,
    say that you could not find enough information in the document.
    """