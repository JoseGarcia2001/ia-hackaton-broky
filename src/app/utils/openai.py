"""
OpenAI utils
"""
from app.config import settings
from openai import OpenAI
from loguru import logger


class OpenIA:
    def __init__(self):
        self.openai_client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
        )

    def extract_text_audio(self, audio_path: str) -> str:
        """Extract text from an audio file"""
        with open(audio_path, "rb") as f:
            try:
                transcription = self.openai_client.audio.transcriptions.create(
                    file=f,
                    model="whisper-1",
                )
                text = transcription.text
                logger.info(f"Text extracted from audio: {text}")
                return text
            except Exception as e: # pylint: disable=broad-exception-caught
                logger.error(f"Error extracting text from audio: {str(e)}")
                return ""
