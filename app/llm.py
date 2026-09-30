import os
from dotenv import load_dotenv
from google import genai
from google.genai import errors

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_answer(question: str, context: str) -> str:
    prompt = f"""
    Answer the user's question using only the document context below.

    Use direct evidence from the context when available.
    You may also make reasonable interpretations or inferences when they are
    strongly supported by the context.

    Do not introduce facts and outside sources that are not supported by the document.

    When you use information from a source, cite it using the source label
    exactly as written, for example [Source 1] or [Source 2].

    If the answer is not stated explicitly but can be reasonably inferred,
    explain that it is an interpretation and support it with the relevant sources.

    Context:
    {context}

    Question:
    {question}

    If the context truly does not contain enough evidence to answer or reasonably
    infer an answer, say that you could not find enough information in the document.

    """

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        print(response)

        if response.text:
            return response.text

        return "The AI returned an empty response."

    except errors.ServerError:
        return "The AI service is temporarily unavailable. Please try again."