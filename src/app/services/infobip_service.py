import httpx
import logging
from typing import Dict, Any, Optional
from app.config import settings
from app.models.whatsapp import (
    WhatsAppResponse,
    WhatsAppError
)

logger = logging.getLogger(__name__)

class InfobipService:
    """Service for interacting with Infobip WhatsApp API"""
    
    def __init__(self):
        self.api_key = settings.INFOBIP_API_KEY
        self.base_url = settings.INFOBIP_BASE_URL
        self.whatsapp_from = settings.INFOBIP_WHATSAPP_FROM
        
        if not self.api_key:
            raise ValueError("INFOBIP_API_KEY is not configured")
        if not self.whatsapp_from:
            raise ValueError("INFOBIP_WHATSAPP_FROM is not configured")
    
    def _get_headers(self) -> Dict[str, str]:
        """Get the necessary headers for Infobip requests"""
        return {
            "Authorization": f"App {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    async def send_text_message(self, to: str, text: str) -> WhatsAppResponse:
        """
        Send a text message via WhatsApp
        
        Args:
            to: Recipient phone number
            text: Message text
            
        Returns:
            WhatsAppResponse with API response
        """
        try:
            message_data = {
                "messages": [
                    {
                        "from": self.whatsapp_from,
                        "to": to,
                        "content": {
                            "text": text
                        }
                    }
                ]
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/whatsapp/1/message",
                    headers=self._get_headers(),
                    json=message_data,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    return WhatsAppResponse(**response.json())
                else:
                    error_data = response.json()
                    logger.error(f"Error sending message: {error_data}")
                    raise WhatsAppError(**error_data)
                    
        except Exception as e:
            logger.error(f"Error in send_text_message: {str(e)}")
            raise
    
    async def send_template_message(
        self, 
        to: str, 
        template_name: str, 
        language: str = "en",
        template_data: Optional[Dict[str, Any]] = None
    ) -> WhatsAppResponse:
        """
        Send a template message via WhatsApp
        
        Args:
            to: Recipient phone number
            template_name: Template name
            language: Template language
            template_data: Data to fill the template
            
        Returns:
            WhatsAppResponse with API response
        """
        try:
            message_data = {
                "messages": [
                    {
                        "from": self.whatsapp_from,
                        "to": to,
                        "content": {
                            "templateName": template_name,
                            "language": language
                        }
                    }
                ]
            }
            
            if template_data:
                message_data["messages"][0]["content"]["templateData"] = template_data
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/whatsapp/1/message",
                    headers=self._get_headers(),
                    json=message_data,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    return WhatsAppResponse(**response.json())
                else:
                    error_data = response.json()
                    logger.error(f"Error sending template: {error_data}")
                    raise WhatsAppError(**error_data)
                    
        except Exception as e:
            logger.error(f"Error in send_template_message: {str(e)}")
            raise
