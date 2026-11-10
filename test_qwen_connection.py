
import os
import base64
from io import BytesIO

from dotenv import load_dotenv
from PIL import Image
from huggingface_hub import InferenceClient

# 1. Load environment variables
load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise ValueError("HF_TOKEN not found in .env")

# 2. Define the model
MODEL_ID = "Qwen/Qwen2.5-VL-7B-Instruct"

# 3. Initialise Hugging Face inference client
client = InferenceClient(
    provider="featherless-ai",
    token=HF_TOKEN
)

# 4. Load the local image
image = Image.open("sample.jpg").convert("RGB")

# 5. Convert image to JPEG bytes
image_buffer = BytesIO()
image.save(image_buffer, format="JPEG")

image_bytes = image_buffer.getvalue()

# 6. Encode image bytes as Base64
base64_image = base64.b64encode(
    image_bytes
).decode("utf-8")

# 7. Create a data URL
image_data_url = (
    f"data:image/jpeg;base64,{base64_image}"
)

# 8. Prepare the multimodal message
messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "image_url",
                "image_url": {
                    "url": image_data_url
                }
            },
            {
                "type": "text",
                "text": "Describe what you see in this image."
            }
        ]
    }
]

print("Sending image to Qwen2.5-VL...")

# 9. Send request to the model
response = client.chat_completion(
    model=MODEL_ID,
    messages=messages,
    max_tokens=200
)

# 10. Extract the model response
caption = response.choices[0].message.content

print("\nModel Response:")
print(caption)
