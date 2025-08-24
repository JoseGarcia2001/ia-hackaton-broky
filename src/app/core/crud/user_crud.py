from typing import List, Optional, Dict, Any
from pymongo.database import Database
from bson import ObjectId
from datetime import datetime

from ...models import User, UserRole, AvailabilitySlot


class UserCRUD:
    """CRUD operations for User collection"""
    
    def __init__(self, db: Database):
        self.collection = db.users
    
    def get_user_type(self, phone_number: str) -> str:
        """
        Determine user type based on phone number
        Check if user exists in database - registered users are sellers, others are buyers
        """
        # Check if user exists in database
        user_doc = self.collection.find_one({"phone": phone_number})
        
        if user_doc:
            return "seller"
        else:
            return "buyer"
    
    def get_or_create_user(self, phone: str, name: str = None) -> User:
        """
        Get existing user or create new one
        """
        # Mock implementation for now
        return User(
            id=f"user_{phone}",
            name=name or f"User {phone}",
            phone=phone,
            role=UserRole.BUYER,
            created_at=datetime.utcnow()
        )
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """
        Get user by ID
        
        Args:
            user_id: User's ID
            
        Returns:
            Optional[User]: User object if found, None otherwise
        """
        try:
            user_doc = self.collection.find_one({"_id": ObjectId(user_id)})
            if user_doc:
                user_doc["_id"] = str(user_doc["_id"])
                return User(**user_doc)
            return None
        except Exception as e:
            print(f"Error getting user by id: {e}")
            return None
    
    def add_availability(self, user_id: str, availability_slots: List[AvailabilitySlot]) -> bool:
        """
        Add availability slots to a user's schedule
        
        Args:
            user_id: User's ID
            availability_slots: List of availability slots
            
        Returns:
            bool: True if successfully added, False otherwise
        """
        try:
            slots_data = [slot.dict() for slot in availability_slots]
            result = self.collection.update_one(
                {"_id": ObjectId(user_id)},
                {
                    "$push": {"availability": {"$each": slots_data}},
                    "$set": {"updated_at": datetime.utcnow()}
                }
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error adding availability: {e}")
            return False
    
    def check_availability(self, user_id: str, start_time: datetime, end_time: datetime) -> bool:
        """
        Check if a user is available during a specific time period
        
        Args:
            user_id: User's ID
            start_time: Start of the time period to check
            end_time: End of the time period to check
            
        Returns:
            bool: True if user is available (no conflicts), False if busy
        """
        try:
            user_doc = self.collection.find_one({"_id": ObjectId(user_id)})
            if not user_doc or not user_doc.get("availability"):
                return True
            
            for slot in user_doc["availability"]:
                slot_start = datetime.fromisoformat(slot["start_time"].replace("Z", "+00:00"))
                slot_end = datetime.fromisoformat(slot["end_time"].replace("Z", "+00:00"))
                
                if (start_time < slot_end and end_time > slot_start):
                    return False
            
            return True
        except Exception as e:
            print(f"Error checking availability: {e}")
            return False
    
    def get_user_availability(self, user_id: str) -> List[AvailabilitySlot]:
        """
        Get all availability slots for a user
        
        Args:
            user_id: User's ID
            
        Returns:
            List[AvailabilitySlot]: List of availability slots
        """
        try:
            user_doc = self.collection.find_one({"_id": ObjectId(user_id)})
            if not user_doc or not user_doc.get("availability"):
                return []
            
            return [AvailabilitySlot(**slot) for slot in user_doc["availability"]]
        except Exception as e:
            print(f"Error getting availability: {e}")
            return []
    
    def get_user_by_phone(self, phone: str) -> Optional[User]:
        """
        Get user by phone number
        
        Args:
            phone: User's phone number
            
        Returns:
            Optional[User]: User object if found, None otherwise
        """
        try:
            user_doc = self.collection.find_one({"phone": phone})
            if user_doc:
                user_doc["_id"] = str(user_doc["_id"])
                return User(**user_doc)
            return None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
