import google.genai as genai

import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv('Geminiapi'))

# List all available models
for model in client.models.list():
    print(model)
