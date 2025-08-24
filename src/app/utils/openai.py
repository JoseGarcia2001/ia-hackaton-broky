"""
OpenAI utils
"""
from ..config import settings
from openai import OpenAI
from loguru import logger
import base64


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

    def integrate_images(self, data_property) -> str:
        """Integrate images into a property"""

        response = self.openai_client.responses.create(
            model="gpt-4o",
            input="Toma la imagen de la propiedad y integrala con el QR code. Respeta el contenido del QR code.",
            tools=[{"type": "image_generation"}],
        )
        

        image_data = [
            output.result
            for output in response.output
            if output.type == "image_generation_call"
        ]

        if image_data:
            image_base64 = image_data[0]
            with open("cat_and_otter.png", "wb") as f:
                f.write(base64.b64decode(image_base64))
        image_data = [
            output.result
            for output in response.output
            if output.type == "image_generation_call"
        ]

        if image_data:
            image_base64 = image_data[0]
            with open("cat_and_otter.png", "wb") as f:
                f.write(base64.b64decode(image_base64))
