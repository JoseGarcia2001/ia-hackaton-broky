from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class MessageType(str, Enum):
    IMAGE = "image"
    TEXT = "text"
    AUDIO = "audio"


class MessageSender(str, Enum):
    USER = "user"
    SYSTEM = "system"


class Message(BaseModel):
    """Message collection model"""
    id: Optional[str] = Field(None, alias="_id", description="MongoDB ObjectId")
    chat_id: str = Field(..., description="Chat ID this message belongs to")
    sender: MessageSender = Field(..., description="Who sent the message: user or system")
    type: MessageType = Field(..., description="Message type: image, text, or audio")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    is_read: bool = Field(default=False, description="Message read status")

    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }