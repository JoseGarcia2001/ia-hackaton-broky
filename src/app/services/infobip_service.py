import httpx
import logging
from typing import Dict, Any, Optional
from ..config import settings
from ..models.whatsapp import (
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
    
    def receive_webhook_message(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Receive and validate message from Infobip webhook
        
        Args:
            webhook_data: Raw webhook data from Infobip
            
        Returns:
            Dict with processed message information
        """
        try:
            logger.info(f"Received webhook data: {webhook_data}")
            # Validate webhook structure according to Infobip documentation
            if not webhook_data.get("results"):
                logger.warning("Invalid webhook: missing 'results' field")
                return {"valid": False, "error": "Invalid webhook structure"}
            
            processed_messages = []
            
            for result in webhook_data.get("results", []):
                processed_message = self._process_single_message(result)
                if processed_message:
                    processed_messages.append(processed_message)
            
            return processed_messages[0] if processed_messages else {"valid": False, "error": "No valid messages found"}
            
        except Exception as e:
            logger.error(f"Error processing webhook message: {str(e)}")
            return {"valid": False, "error": str(e)}
    
    def _process_single_message(self, result: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process a single message result from Infobip webhook
        
        Args:
            result: Single result from webhook according to Infobip structure
            
        Returns:
            Dict with processed message info or None if invalid
        """
        try:
            # Extract data according to Infobip webhook structure
            message_id = result.get("messageId")
            from_number = result.get("sender")
            to_number = result.get("destination")
            received_at = result.get("receivedAt")
            event = result.get("event")
            channel = result.get("channel")
            content_list = result.get("content", [])
            
            if not all([message_id, from_number, content_list]):
                logger.warning(f"Incomplete message data: {result}")
                return None
            
            # Get the first content item (Infobip sends array but usually has one item)
            message_data = content_list[0] if content_list else {}
            message_type = message_data.get("type", "unknown").lower()
            
            # Validate and extract content based on message type
            message_content = self._extract_message_content(message_data, message_type)
            
            return {
                "id": message_id,
                "from": from_number,
                "to": to_number,
                "received_at": received_at,
                "event": event,
                "channel": channel,
                "type": message_type,
                "content": message_content,
                "is_valid": message_content is not None
            }
            
        except Exception as e:
            logger.error(f"Error processing single message: {str(e)}")
            return None
    
    def _extract_message_content(self, message_data: Dict[str, Any], message_type: str) -> Optional[Dict[str, Any]]:
        """
        Extract content based on message type according to Infobip structure
        
        Args:
            message_data: Message data from Infobip webhook
            message_type: Type of message (lowercased)
            
        Returns:
            Dict with extracted content or None if invalid
        """
        try:
            content = {}
            
            if message_type == "text":
                # For TEXT messages, text and cleanText are directly in message_data
                content = {
                    "text": message_data.get("text", ""),
                    "clean_text": message_data.get("cleanText", ""),
                    "keyword": message_data.get("keyword"),
                    "type": "text"
                }
                
            elif message_type == "image":
                # For IMAGE messages
                content = {
                    "url": message_data.get("url", ""),
                    "type": "image"
                }
                
            elif message_type == "audio":
                # For AUDIO messages
                content = {
                    "url": message_data.get("url", ""),
                    "type": "audio"
                }
      
            else:
                logger.warning(f"Unsupported message type: {message_type}")
                content = {
                    "raw_data": message_data,
                    "type": "unsupported"
                }
            
            return content if content else None
            
        except Exception as e:
            logger.error(f"Error extracting content for type {message_type}: {str(e)}")
            return None
