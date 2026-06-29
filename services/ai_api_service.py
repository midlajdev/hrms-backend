import logging

logger = logging.getLogger(__name__)


class AIService:
    def generate_reply(self, prompt):
        try:
            return {
                "status": "success",
                "response": "Hello candidate"
            }
        except Exception as e:
            logger.error(
                f"Generate reply error: {str(e)}"
            )
            return {
                "status": "error",
                "response": "Fallback response"
            }
        
    def speech_to_text(self, audio):
        try:
            return {
                "status": "success",
                "text": "Mock converted text"
            }
        except Exception as e:

            logger.error(
                f"Speech to text error: {str(e)}"
            )
            return {
                "status": "error",
                "text": ""
            }

    def text_to_speech(self, text):
        try:
            return {
                "status": "success",
                "audio": "mock_audio_url"
            }
        except Exception as e:
            logger.error(
                f"Text to speech error: {str(e)}"
            )
            return {
                "status": "error",
                "audio": None
            }