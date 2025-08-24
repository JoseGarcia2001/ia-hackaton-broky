from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, time
from enum import Enum


class UserRole(str, Enum):
    BUYER = "buyer"
    SELLER = "seller"


class AvailabilitySlot(BaseModel):
    """Model for recurring weekly time slots"""
    day_of_week: int = Field(..., ge=0, le=6, description="Day of week (0=Monday, 6=Sunday)")
    start_time: time = Field(..., description="Start time")
    end_time: time = Field(..., description="End time")
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