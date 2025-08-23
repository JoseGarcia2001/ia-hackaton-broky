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
            # Validate webhook structure according to Infobip documentation
            if not webhook_data.get("results"):
                logger.warning("Invalid webhook: missing 'results' field")
                return {"valid": False, "error": "Invalid webhook structure"}
            
            processed_messages = []
            
            for result in webhook_data.get("results", []):
                processed_message = self._process_single_message(result)
                if processed_message:
                    processed_messages.append(processed_message)
            
            return processed_messages[0]
            
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
            from_number = result.get("from")
            to_number = result.get("to")
            received_at = result.get("receivedAt")
            integration_type = result.get("integrationType")
            message_data = result.get("message", {})
            contact_data = result.get("contact", {})
            
            if not all([message_id, from_number, message_data]):
                logger.warning(f"Incomplete message data: {result}")
                return None
            
            message_type = message_data.get("type", "unknown").lower()
            
            # Validate and extract content based on message type
            message_content = self._extract_message_content(message_data, message_type)
            
            return {
                "id": message_id,
                "from": from_number,
                "to": to_number,
                "received_at": received_at,
                "integration_type": integration_type,
                "type": message_type,
                "content": message_content,
                "contact": {
                    "name": contact_data.get("name", "")
                },
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
                # For TEXT messages, content is directly in the message
                content = {
                    "text": message_data.get("text", ""),
                    "type": "text"
                }
                
            elif message_type == "image":
                # For IMAGE messages
                image_data = message_data.get("image", {})
                content = {
                    "url": image_data.get("url", ""),
                    "caption": image_data.get("caption", ""),
                    "mime_type": image_data.get("mimeType", ""),
                    "type": "image"
                }
                
            elif message_type == "audio":
                # For AUDIO messages
                audio_data = message_data.get("audio", {})
                content = {
                    "url": audio_data.get("url", ""),
                    "mime_type": audio_data.get("mimeType", ""),
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
    
    def validate_message_type(self, message_type: str) -> bool:
        """
        Validate if message type is supported according to Infobip documentation
        
        Args:
            message_type: Type of message to validate
            
        Returns:
            True if supported, False otherwise
        """
        supported_types = [
            "text", 
            "image", 
            "video",
            "audio", 
            "document", 
            "location", 
            "contact",
            "button_reply",
            "list_reply",
            "order",
            "sticker"
        ]
        return message_type.lower() in supported_types
    
    def get_message_summary(self, processed_message: Dict[str, Any]) -> str:
        """
        Get a human-readable summary of the message
        
        Args:
            processed_message: Processed message data
            
        Returns:
            String summary of the message
        """
        try:
            message_type = processed_message.get("type", "unknown")
            content = processed_message.get("content", {})
            contact_name = processed_message.get("contact", {}).get("name", "Unknown")
            
            if message_type == "text":
                text = content.get('text', '')
                return f"Text from {contact_name}: {text[:50]}{'...' if len(text) > 50 else ''}"
            elif message_type == "image":
                caption = content.get('caption', '')
                return f"Image from {contact_name}{f' with caption: {caption[:30]}...' if caption else ''}"
            elif message_type == "audio":
                return f"Audio message from {contact_name}"
            elif message_type == "video":
                caption = content.get('caption', '')
                return f"Video from {contact_name}{f' with caption: {caption[:30]}...' if caption else ''}"
            elif message_type == "document":
                filename = content.get('filename', 'Unknown file')
                return f"Document from {contact_name}: {filename}"
            elif message_type == "location":
                name = content.get('name', 'Unknown location')
                return f"Location from {contact_name}: {name}"
            elif message_type == "contact":
                return f"Contact shared by {contact_name}"
            elif message_type == "button_reply":
                title = content.get('title', '')
                return f"Button reply from {contact_name}: {title}"
            elif message_type == "list_reply":
                title = content.get('title', '')
                return f"List selection from {contact_name}: {title}"
            else:
                return f"Unsupported message type from {contact_name}: {message_type}"
                
        except Exception as e:
            logger.error(f"Error creating message summary: {str(e)}")
            return "Error processing message"
