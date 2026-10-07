import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY"),
    http_options=types.HttpOptions(
        timeout=10000
    )
)


def generate_answer(question, retrieved_chunks):

    context = "\n\n".join(
        [
            chunk["content"]
            for chunk in retrieved_chunks
        ]
    )

    prompt = f"""
You are a construction knowledge assistant.

Answer the user's question using ONLY the provided context.

If the answer is not available in the context, say:

"I don't have enough information in the knowledge base."

Context:
{context}

User Question:
{question}

Answer clearly and concisely.
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0,
                max_output_tokens=300
            )
        )

        return response.text

    except Exception as e:

        error_message = str(e)

        if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:
            return (
                "⚠️ Gemini API quota has been exhausted.\n\n"
                "The RAG retrieval is working correctly, "
                "but the Gemini API quota is currently unavailable."
            )

        if "503" in error_message or "UNAVAILABLE" in error_message:
            return (
                "⚠️ Gemini is temporarily unavailable.\n\n"
                "Please try again later."
            )

        return f"❌ Gemini API Error: {error_message}"