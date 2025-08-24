import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    # Infobip Configuration
    INFOBIP_API_KEY: str = os.getenv("INFOBIP_API_KEY", "")
    INFOBIP_BASE_URL: str = os.getenv("INFOBIP_BASE_URL", "https://api.infobip.com")
    INFOBIP_WHATSAPP_FROM: str = os.getenv("INFOBIP_WHATSAPP_FROM", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    AWS_ACCESS_KEY: str = os.getenv("AWS_ACCESS_KEY", "")
    AWS_SECRET_KEY: str = os.getenv("AWS_SECRET_KEY", "")
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")

settings = Settings()
