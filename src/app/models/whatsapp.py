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
class WhatsAppResponse(BaseModel):
    """Model for sending response"""
    messages: List[Dict[str, str]]
    bulk_id: Optional[str] = None

class WhatsAppError(BaseModel):
    """Model for WhatsApp errors"""
    requestError: Dict[str, Any]
