from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from .business_stage import SellerStage


class LegalDocument(BaseModel):
    """Model for legal documents"""
    doc_type: str = Field(..., description="Type of document")
    link: str = Field(..., description="Link or path to document")
    upload_date: Optional[datetime] = Field(default_factory=datetime.utcnow)


class Property(BaseModel):
    """Property collection model"""
    id: Optional[str] = Field(None, alias="_id", description="MongoDB ObjectId")
    address: str = Field(..., description="Property address")
    type: Optional[str] = Field(None, description="Property type (apartment, house, etc.)")
    images: List[str] = Field(default_factory=list, description="Base64 encoded images")
    legal_docs: List[LegalDocument] = Field(default_factory=list, description="Legal documents")
    value: float = Field(..., description="Property value")
    description: str = Field(..., description="Property description")
    amenities: List[str] = Field(default_factory=list, description="Property amenities")
    nearby_places: List[str] = Field(default_factory=list, description="Nearby places of interest")
    owner_id: str = Field(..., description="Owner's user ID")
    business_stage: SellerStage = Field(default=SellerStage.REGISTRATION, description="Business stage of the property")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(None)
    is_active: bool = Field(default=True, description="Property is available for sale")

    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }