import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("Error: No API key found in environment.")
else:
    client = genai.Client(api_key=api_key)
    print(f"Checking models (google-genai SDK) for key starting with: {api_key[:5]}...")
    try:
        # list_models returns an iterator of Model objects
        for m in client.models.list():
            print(f"Model ID: {m.name}, Display Name: {m.display_name}")
            print(f"  Supported Actions: {m.supported_actions}")
    except Exception as e:
        print(f"Error listing models: {e}")
