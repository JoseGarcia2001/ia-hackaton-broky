from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

from ..core.crud.property_crud import PropertyCRUD
from ..core.database import get_db
from ..models.property import Property
from ..models.business_stage import SellerStage


class PropertyInfo(BaseModel):
    """
    Información mínima para registrar una propiedad.
    """
    address: Optional[str] = Field(description="Dirección de la propiedad")
    type: Optional[str] = Field(description="Tipo de propiedad")
    price: Optional[float] = Field(description="Precio de la propiedad")
    description: Optional[str] = Field(description="Descripción de la propiedad")
    pictures: Optional[list[str]] = Field(description="Fotos de la propiedad")


class PropertyProgress(BaseModel):
    property_id: str
    current_stage: str
    missing_fields: list
    completion_percentage: float


class PropertyService:
    """Service layer for property operations"""
    
    def __init__(self):
        db = get_db()
        self.property_crud = PropertyCRUD(db)
    
    def create_property(self, info: PropertyInfo, owner_id: str) -> Optional[Property]:
        """Create a new property with initial data and return the full property"""
        # Convert PropertyInfo to property data
        property_data = {
            "address": info.address,
            "type": info.type,
            "value": float(info.price) if info.price else 0.0,
            "owner_id": owner_id,
        }
        
        property_id = self.property_crud.create_property(property_data)
        return self.property_crud.get_property_by_id(property_id)
    
    def get_property_id_by_address(self, address: str) -> Optional[Property]:
        """Get property by address, returns full property object like create"""
        property_obj = self.property_crud.get_property_by_address(address)
        return property_obj
    
    def update_property(self, property_id: str, update_data: Dict[str, Any]) -> bool:
        """Update property with partial fields"""
        return self.property_crud.update_property_partial(property_id, update_data)
    
    def get_progress_info(self, property_id: str) -> Optional[PropertyProgress]:
        """Get property progress info with missing fields"""
        progress_data = self.property_crud.get_property_missing_fields(property_id)
        
        if progress_data:
            return PropertyProgress(
                property_id=progress_data["property_id"],
                current_stage=progress_data["current_stage"],
                missing_fields=progress_data["missing_fields"],
                completion_percentage=progress_data["completion_percentage"]
            )
        
        return None
    
    def get_property_full_info(self, property_id: str) -> Optional[Property]:
        """Get complete property information"""
        return self.property_crud.get_property_by_id(property_id)