from pydantic import BaseModel, Field

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
