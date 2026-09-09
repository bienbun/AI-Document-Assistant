import os
from dotenv import load_dotenv
from google import genai

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

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text