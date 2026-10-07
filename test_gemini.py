import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

print("STEP 1: Gemini client created")
print("STEP 2: Calling Gemini...")

response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Say hello in one sentence."
)

print("STEP 3: Gemini response received")
print(response.text)