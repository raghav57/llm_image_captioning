
import os
from dotenv import load_dotenv
from PIL import Image
from google import genai

# 1. Load environment variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")

# 2. Initialise Gemini client
client = genai.Client(api_key=API_KEY)

print("Gemini client initialised successfully!")

# 3. Load sample image
image = Image.open("sample.jpg").convert("RGB")

print("Image loaded successfully:", image.size)

# 4. Define the prompt
prompt = """
Describe this image.

Identify:
1. The main subject
2. The surroundings
3. Important visual details

Write a clear and concise description.
"""

# 5. Send image and prompt to Gemini
response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=[prompt, image]
)

# 6. Display the response
print("\nGemini Image Description:")
print(response.text)
