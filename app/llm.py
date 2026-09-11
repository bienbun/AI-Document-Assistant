import os
from dotenv import load_dotenv
from google import genai
from google.genai import errors

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_answer(question: str, context: str) -> str:
    prompt = f"""
You are answering questions using only the document context below.

Context:
{context}

Question:
{question}

If the answer cannot be found in the context, say that you could not find it in the document.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        return response.text

    except errors.ServerError:
        return "The AI service is temporarily unavailable. Please try again."