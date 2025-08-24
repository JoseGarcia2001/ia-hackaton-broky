from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .business_stage import BuyerStage


class Chat(BaseModel):
    """Chat collection model - conversation between system and a user"""
    id: Optional[str] = Field(None, alias="_id", description="MongoDB ObjectId")
    user_id: str = Field(..., description="User ID participating in the chat")
    user_phone: Optional[str] = Field(None, description="User's phone number for quick lookup")
    property_id: Optional[str] = Field(None, description="Related property ID (if applicable)")
    business_stage: Optional[BuyerStage] = Field(None, description="Business stage for buyer interactions")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(None)
    is_active: bool = Field(default=True, description="Chat is active")

    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }