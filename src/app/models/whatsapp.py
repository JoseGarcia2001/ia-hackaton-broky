from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

# Models for sending messages
class WhatsAppTextMessage(BaseModel):
    """Model for WhatsApp text message"""
    to: str = Field(..., description="Recipient phone number")
    text: str = Field(..., description="Message text")

class WhatsAppTemplateMessage(BaseModel):
    """Model for WhatsApp template message"""
    to: str = Field(..., description="Recipient phone number")
    template_name: str = Field(..., description="Template name")
    language: str = Field(..., description="Template language (e.g., en)")
    template_data: Optional[Dict[str, Any]] = Field(None, description="Template data")

class WhatsAppMessageRequest(BaseModel):
    """Model for message sending request"""
    messages: List[WhatsAppTextMessage]

class WhatsAppTemplateRequest(BaseModel):
    """Model for template sending request"""
    messages: List[WhatsAppTemplateMessage]

# Response models
class MessageStatus(BaseModel):
    """Model for message status"""
    groupId: int
    groupName: str
    id: int
    name: str
    description: str

class WhatsAppResponse(BaseModel):
    """Model for sending response from Infobip"""
    to: str = Field(..., description="Recipient phone number")
    messageCount: int = Field(..., description="Number of messages sent")
    messageId: str = Field(..., description="Unique message identifier")
    status: MessageStatus = Field(..., description="Message status information")

class WhatsAppError(Exception):
    """Exception for WhatsApp errors"""
    def __init__(self, **kwargs):
        self.request_error = kwargs.get('requestError', kwargs)
        error_message = f"WhatsApp API Error: {self.request_error}"
        super().__init__(error_message)
