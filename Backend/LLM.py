import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class LLM:
    def __init__(self, model_name="gemini-2.0-flash-lite-001", temperature=0):
        """
        Initialize the Gemini LLM with model name and temperature.
        """
        genai.configure(api_key=os.getenv("Geminiapi"))
        self.model = genai.GenerativeModel(model_name)
        self.temperature = temperature

    def invoke(self, prompt: str) -> str:
        """
        Generate content using the Gemini model.
        Takes a plain string prompt and returns the response text.
        """
        response = self.model.generate_content(
            prompt,
            generation_config={"temperature": self.temperature}
        )
        return response.text.strip()
