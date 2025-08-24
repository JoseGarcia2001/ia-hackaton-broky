from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel, Field

from ..core.crud.user_crud import UserCRUD
from ..core.database import get_db
from ..models.user import User, AvailabilitySlot


class BuyerInfo(BaseModel):
    """
    Información mínima para registrar un comprador.
    """
    name: Optional[str] = Field(description="Nombre del comprador")


class BuyerProgress(BaseModel):
    user_id: str
    current_stage: str
    missing_fields: list
    completion_percentage: float


class UserService:
    """Service layer for user operations including availability management"""
    
    def __init__(self):
        db = get_db()
        self.user_crud = UserCRUD(db)
    
    def add_availability(self, user_id: str, availability_slots: List[AvailabilitySlot]) -> bool:
        """
        Add availability slots to a user's schedule
        
        Args:
            user_id: User's ID
            availability_slots: List of availability slots to add
            
        Returns:
            bool: True if successfully added, False otherwise
        """
        return self.user_crud.add_availability(user_id, availability_slots)
    
    def check_user_availability(self, user_id: str, start_time: datetime, end_time: datetime) -> bool:
        """
        Check if a user is available during a specific time period
        
        Args:
            user_id: User's ID
            start_time: Start of the time period to check
            end_time: End of the time period to check
            
        Returns:
            bool: True if user is available (no conflicts), False if busy
        """
        
        return self.user_crud.check_availability(user_id, start_time, end_time)
    
    def get_user_availability(self, user_id: str) -> List[AvailabilitySlot]:
        """
        Get all availability slots for a user
        
        Args:
            user_id: User's ID
            
        Returns:
            List[AvailabilitySlot]: List of availability slots
        """
        return self.user_crud.get_user_availability(user_id)
    
    def update_buyer_info(self, user_id: str, buyer_info: BuyerInfo) -> bool:
        """Update buyer information (currently just name)"""
        update_data = {}
        
        if buyer_info.name:
            update_data["name"] = buyer_info.name
        
        if update_data:
            return self.user_crud.update_user_partial(user_id, update_data)
        
        return False
    
    def get_buyer_progress(self, user_id: str) -> Optional[BuyerProgress]:
        """Get buyer progress info with missing fields"""
        progress_data = self.user_crud.get_user_missing_fields(user_id)
        
        if progress_data:
            return BuyerProgress(
                user_id=progress_data["user_id"],
                current_stage=progress_data["current_stage"],
                missing_fields=progress_data["missing_fields"],
                completion_percentage=progress_data["completion_percentage"]
            )
        
        return None
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return self.user_crud.get_user_by_id(user_id)
