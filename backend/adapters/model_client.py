import os
from abc import ABC, abstractmethod

import dotenv
import google.generativeai as genai


class ModelClient(ABC):
    @abstractmethod
    def execute(self, prompt: str) -> str:
        pass


class GeminiModelClient(ModelClient):
    def __init__(self):
        dotenv.load_dotenv()
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not gemini_api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def execute(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text