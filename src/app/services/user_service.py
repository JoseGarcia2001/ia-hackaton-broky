from typing import List, Optional
from datetime import datetime, timedelta

from ..core.crud.user_crud import UserCRUD
from ..core.database import get_db
from ..models.user import User, AvailabilitySlot


class UserService:
    """Service layer for user operations including availability management"""
    
    def __init__(self):
        db = get_db()
        self.user_crud = UserCRUD(db)
    
    async def add_availability(self, user_id: str, availability_slots: List[AvailabilitySlot]) -> bool:
        """
        Add availability slots to a user's schedule
        
        Args:
            user_id: User's ID
            availability_slots: List of availability slots to add
            
        Returns:
            bool: True if successfully added, False otherwise
        """
        return self.user_crud.add_availability(user_id, availability_slots)
    
    async def check_user_availability(self, user_id: str, start_time: datetime, end_time: datetime) -> bool:
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
    
    async def get_user_availability(self, user_id: str) -> List[AvailabilitySlot]:
        """
        Get all availability slots for a user
        
        Args:
            user_id: User's ID
            
        Returns:
            List[AvailabilitySlot]: List of availability slots
        """
        return self.user_crud.get_user_availability(user_id)
    
