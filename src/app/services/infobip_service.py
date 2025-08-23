import requests
import logging
<<<<<<< Updated upstream
=======
import httpx
import uuid
import os
from pathlib import Path
from urllib.parse import urlparse
>>>>>>> Stashed changes
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
        self.base_url = f"https://{settings.INFOBIP_BASE_URL}"
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
    
    def send_text_message(self, to: str, text: str) -> WhatsAppResponse:
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
                "from": self.whatsapp_from,
                "to": to,
                "content": {
                    "text": text
                }
            }

            response = requests.post(
                f"{self.base_url}/whatsapp/1/message/text",
                headers=self._get_headers(),
                json=message_data,
                timeout=30.0
            )

            if response.status_code == 200:
                return WhatsAppResponse(**response.json())
            else:
                try:
                    error_data = response.json()
                except:
                    error_data = {"error": f"HTTP {response.status_code}: {response.text}"}
                logger.error(f"Error sending message: {error_data}")
                raise WhatsAppError(**error_data)
                
        except Exception as e:
            logger.error(f"Error in send_text_message: {str(e)}")
            raise
    
    def send_template_message(
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
                "from": self.whatsapp_from,
                "to": to,
                "content": {
                    "templateName": template_name,
                    "language": language
                }
            }
            
            if template_data:
                message_data["content"]["templateData"] = template_data
            
            response = requests.post(
                f"{self.base_url}/whatsapp/1/message",
                headers=self._get_headers(),
                json=message_data,
                timeout=30.0
            )
            
            if response.status_code == 200:
                return WhatsAppResponse(**response.json())
            else:
                try:
                    error_data = response.json()
                except:
                    error_data = {"error": f"HTTP {response.status_code}: {response.text}"}
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
            url = result.get("url")
            
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
                "is_valid": message_content is not None,
                "url": url
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

    def save_file(self, url: str, path: str) -> str:
        """
        Save a file from a URL
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
            "sticker",
        ]
        return message_type.lower() in supported_types

    async def download_file_content(self, file_url: str) -> bytes:
        """
        Download file content from Infobip URL
        
        Args:
            file_url: URL of the file to download from Infobip
            
        Returns:
            bytes: File content
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    file_url,
                    headers={"Authorization": f"App {self.api_key}"},
                    timeout=30.0,
                )
                response.raise_for_status()
                return response.content
        except Exception as e: # pylint: disable=broad-exception-caught
            logger.error(f"Error downloading file from {file_url}: {str(e)}")
            raise

    def _get_file_extension(self, mime_type: str, content_type: str) -> str:
        """
        Determine file extension based on mime_type or content type
        
        Args:
            mime_type: MIME type from message content
            content_type: Content type (audio, image, etc.)
            
        Returns:
            str: File extension with dot (e.g., '.jpg', '.mp3')
        """
        # Mapping of mime types to extensions
        mime_extensions = {
            'image/jpeg': '.jpg',
            'image/jpg': '.jpg', 
            'image/png': '.png',
            'image/gif': '.gif',
            'image/webp': '.webp',
            'image/bmp': '.bmp',
            'image/tiff': '.tiff',
            'audio/mpeg': '.mp3',
            'audio/mp3': '.mp3',
            'audio/mp4': '.mp4',
            'audio/ogg': '.ogg',
            'audio/wav': '.wav',
            'audio/webm': '.webm',
            'audio/aac': '.aac',
            'video/mp4': '.mp4',
            'video/mpeg': '.mpeg',
            'video/webm': '.webm',
            'video/avi': '.avi',
            'video/mov': '.mov',
            
            # Documents
            'application/pdf': '.pdf',
            'application/msword': '.doc',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
        }
        
        # Try to get extension from mime_type first
        if mime_type and mime_type in mime_extensions:
            return mime_extensions[mime_type]
            
        # Fallback to content type defaults
        if content_type == 'image':
            return '.jpg'  # Default image extension
        elif content_type == 'audio':
            return '.mp3'  # Default audio extension  
        elif content_type == 'video':
            return '.mp4'  # Default video extension
        else:
            return '.bin'  # Generic binary extension

    async def save_file(self, url: str, mime_type: str = "", content_type: str = "") -> str:
        """
        Download and save file from Infobip URL with unique name
        
        Args:
            url: URL of the file to download
            mime_type: MIME type of the file
            content_type: Type of content (audio, image, etc.)
            
        Returns:
            str: Complete path to saved file
        """
        try:
            unique_id = str(uuid.uuid4())
            file_extension = self._get_file_extension(mime_type, content_type)
            filename = f"{unique_id}{file_extension}"
            metadata_dir = Path("src/app/resources/metadata")
            metadata_dir.mkdir(parents=True, exist_ok=True)
            file_path = metadata_dir / filename
            file_content = await self.download_file_content(url)
            with open(file_path, "wb") as f:
                f.write(file_content)
            logger.info(f"File saved successfully: {file_path}")
            return str(file_path)
            
        except Exception as e:
            logger.error(f"Error saving file from {url}: {str(e)}")
            raise

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
                text = content.get("text", "")
                return f"Text from {contact_name}: {text[:50]}{'...' if len(text) > 50 else ''}"
            elif message_type == "image":
                caption = content.get("caption", "")
                return f"Image from {contact_name}{f' with caption: {caption[:30]}...' if caption else ''}"
            elif message_type == "audio":
                return f"Audio message from {contact_name}"
            elif message_type == "video":
                caption = content.get("caption", "")
                return f"Video from {contact_name}{f' with caption: {caption[:30]}...' if caption else ''}"
            elif message_type == "document":
                filename = content.get("filename", "Unknown file")
                return f"Document from {contact_name}: {filename}"
            elif message_type == "location":
                name = content.get("name", "Unknown location")
                return f"Location from {contact_name}: {name}"
            elif message_type == "contact":
                return f"Contact shared by {contact_name}"
            elif message_type == "button_reply":
                title = content.get("title", "")
                return f"Button reply from {contact_name}: {title}"
            elif message_type == "list_reply":
                title = content.get("title", "")
                return f"List selection from {contact_name}: {title}"
            else:
                return f"Unsupported message type from {contact_name}: {message_type}"

        except Exception as e:
            logger.error(f"Error creating message summary: {str(e)}")
            return "Error processing message"
