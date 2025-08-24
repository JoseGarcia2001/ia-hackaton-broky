from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    BUYER = "buyer"
    SELLER = "seller"


class AvailabilitySlot(BaseModel):
    """Model for time slots"""
    start_time: datetime = Field(..., description="Start time of time slot")
    end_time: datetime = Field(..., description="End time of time slot")
    description: Optional[str] = Field(None, description="Description of time slot")


class User(BaseModel):
    """User collection model"""
    id: Optional[str] = Field(None, alias="_id", description="MongoDB ObjectId")
    name: str = Field(..., description="User's full name")
    phone: str = Field(..., description="User's phone number")
    role: UserRole = Field(..., description="User role: buyer or seller")
    availability: Optional[List[AvailabilitySlot]] = Field(
        None, description="Availability slots (only for sellers)"
    )
    interests: Optional[List[str]] = Field(
        None, description="Property interests (only for buyers)"
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(None)

    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }