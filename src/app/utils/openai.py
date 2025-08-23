"""
OpenAI utils
"""

from app.config import settings
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
            except Exception as e:  # pylint: disable=broad-exception-caught
                logger.error(f"Error extracting text from audio: {str(e)}")
                return ""

    def prettify_image(self, path: str) -> str:
        """Filter an image"""
        with open(path, "rb") as f:
            image_base64 = base64.b64encode(f.read()).decode("utf-8")
        with open("src/app/templates/prompt/images_pretty.txt", "r", encoding="utf-8") as f:
            prompt = f.read()

        response = self.openai_client.responses.create(
            model="gpt-4.1",
            input=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": prompt},
                        {
                            "type": "input_image",
                            "image_url": image_base64,
                        },
                    ],
                }
            ],
            tools=[{"type": "image_generation", "input_fidelity": "high"}],
        )
        image_data = [
            output.result
            for output in response.output
            if output.type == "image_generation_call"
        ]

        if image_data:
            image_base64 = image_data[0]
            with open("src/app/resources/images/filtered_image.png", "wb") as f:
                f.write(base64.b64decode(image_base64))
        return "src/app/resources/images/filtered_image.png"
