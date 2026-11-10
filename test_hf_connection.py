import os

from dotenv import load_dotenv
from huggingface_hub import HfApi, InferenceClient

# Load environment variables
load_dotenv()

# Retrieve Hugging Face token
HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise ValueError("HF_TOKEN not found in .env")

# Authenticate with Hugging Face
api = HfApi(token=HF_TOKEN)

user_info = api.whoami()

print("Authentication successful!")
print("Username:", user_info["name"])

# Initialise inference client
client = InferenceClient(token=HF_TOKEN)

print("Inference client initialised successfully!")