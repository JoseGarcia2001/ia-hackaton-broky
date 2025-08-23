from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class VisitStatus(str, Enum):
    REQUESTED = "requested"
    CONFIRMED = "confirmed"
    CANCELED = "canceled"
    COMPLETED = "completed"


class Visit(BaseModel):
    """Visit collection model"""
    id: Optional[str] = Field(None, alias="_id", description="MongoDB ObjectId")
    property_id: str = Field(..., description="Property ID")
    buyer_id: str = Field(..., description="Buyer's user ID")
    seller_id: str = Field(..., description="Seller's user ID")
    scheduled_at: datetime = Field(..., description="Scheduled visit time")
    status: VisitStatus = Field(default=VisitStatus.REQUESTED, description="Visit status")
    notes: Optional[str] = Field(None, description="Additional notes about the visit")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(None)

    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }