import json
import logging

from django.conf import settings

from google import genai
from google.genai import types

logger = logging.getLogger(__name__)


class GeminiService:
    """
    Service responsible for communicating with the Gemini API.
    """

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )
        self.model = "gemini-2.5-flash"

    def generate_content(self, prompt: str) -> str:
        """
        Returns plain text from Gemini.
        """

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.5,
                    max_output_tokens=1000,
                ),
            )

            return response.text.strip()

        except Exception as e:
            logger.exception("Gemini API Error")
            raise Exception(f"Gemini API Error: {str(e)}")

    def generate_json(self, prompt: str) -> dict:
        """
        Returns a parsed JSON response from Gemini.
        """

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.3,
                    max_output_tokens=1500,
                    response_mime_type="application/json",
                ),
            )

            return json.loads(response.text)

        except Exception as e:
            logger.exception("Gemini API Error")
            raise Exception(f"Gemini API Error: {str(e)}")