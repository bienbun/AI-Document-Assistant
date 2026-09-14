def generate_answer(question: str, context: str) -> str:
    prompt = f"""
Answer the user's question using only the document context below.

You may make reasonable inferences from the context, but do not use
information that is not supported by the document.

Context:
{context}

Question:
{question}

If the context does not contain enough information to answer the question,
say that you could not find enough information in the document.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        return response.text

    except errors.ServerError:
        return "The AI service is temporarily unavailable. Please try again."