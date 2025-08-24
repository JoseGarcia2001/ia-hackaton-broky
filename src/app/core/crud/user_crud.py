from typing import List, Optional, Dict, Any
from pymongo.database import Database
from bson import ObjectId
from datetime import datetime

from ...models import User, UserRole, AvailabilitySlot
from ...utils.logger import logger


class UserCRUD:
    """CRUD operations for User collection"""
    
    def __init__(self, db: Database):
        self.collection = db.users
    
    def get_user_type(self, phone_number: str) -> str:
        """
        Determine user type based on phone number
        Check if user exists in database - registered users are sellers, others are buyers
        """
        logger.info(f"Getting user type for phone {phone_number}")
        # Check if user exists in database
        user_doc = self.collection.find_one({"phone": phone_number})
        
        if user_doc:
            return "seller"
        else:
            return "buyer"
    
    def get_or_create_user(self, phone: str, name: str = None) -> User:
        """
        Get existing user or create new one in database
        """
        logger.info(f"Getting or creating user for phone {phone}")
        # Try to find existing user
        user_doc = self.collection.find_one({"phone": phone})
        
        if user_doc:
            # Return existing user
            return User(
                id=str(user_doc["_id"]),
                name=user_doc["name"],
                phone=user_doc["phone"],
                role=UserRole(user_doc["role"]),
                created_at=user_doc["created_at"]
            )
        else:
            # Create new user in database
            user_data = {
                "name": name or f"User {phone}",
                "phone": phone,
                "role": UserRole.BUYER.value,
                "created_at": datetime.utcnow()
            }
            
            result = self.collection.insert_one(user_data)
            
            return User(
                id=str(result.inserted_id),
                name=user_data["name"],
                phone=phone,
                role=UserRole.BUYER,
                created_at=user_data["created_at"]
            )
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """
        Get user by ID
        
        Args:
            user_id: User's ID
            
        Returns:
            Optional[User]: User object if found, None otherwise
        """
        logger.info(f"Getting user by id {user_id}")
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
        logger.info(f"Adding availability slots to user {user_id}")
        try:
            # Check if user exists first
            user_doc = self.collection.find_one({"_id": ObjectId(user_id)})
            if not user_doc:
                logger.error(f"User {user_id} not found")
                return False
            
            # Convert time objects to strings for MongoDB storage
            slots_data = []
            for slot in availability_slots:
                slot_dict = slot.model_dump()
                # Convert time objects to string format
                slot_dict["start_time"] = slot.start_time.strftime("%H:%M:%S")
                slot_dict["end_time"] = slot.end_time.strftime("%H:%M:%S")
                slots_data.append(slot_dict)
            logger.info(f"Serialized slots data: {slots_data}")
            
            result = self.collection.update_one(
                {"_id": ObjectId(user_id)},
                {
                    "$push": {"availability": {"$each": slots_data}},
                    "$set": {"updated_at": datetime.utcnow()}
                }
            )
            
            logger.info(f"Update result - matched: {result.matched_count}, modified: {result.modified_count}")
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error adding availability: {e}")
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
        logger.info(f"Checking availability for user {user_id}")
        try:
            user_doc = self.collection.find_one({"_id": ObjectId(user_id)})
            if not user_doc or not user_doc.get("availability"):
                return True
            
            # Convert datetime to day_of_week and time for matching
            requested_day = start_time.weekday()  # 0=Monday, 6=Sunday
            requested_start_time = start_time.time()
            requested_end_time = end_time.time()
            
            for slot in user_doc["availability"]:
                slot_day = slot["day_of_week"]
                slot_start_time = datetime.strptime(slot["start_time"], "%H:%M:%S").time()
                slot_end_time = datetime.strptime(slot["end_time"], "%H:%M:%S").time()
                
                # Check if it's the same day and times overlap
                if (requested_day == slot_day and 
                    requested_start_time < slot_end_time and 
                    requested_end_time > slot_start_time):
                    return False  # Conflict found - slot is busy
            
            return True  # No conflicts found
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
        logger.info(f"Getting user availability for user {user_id}")
        try:
            user_doc = self.collection.find_one({"_id": ObjectId(user_id)})
            if not user_doc or not user_doc.get("availability"):
                return []
            
            # Convert stored format to AvailabilitySlot objects
            slots = []
            for slot in user_doc["availability"]:
                try:
                    slot_data = {
                        "day_of_week": slot["day_of_week"],
                        "start_time": datetime.strptime(slot["start_time"], "%H:%M:%S").time(),
                        "end_time": datetime.strptime(slot["end_time"], "%H:%M:%S").time(),
                        "description": slot.get("description")
                    }
                    slots.append(AvailabilitySlot(**slot_data))
                except Exception as slot_error:
                    print(f"Error parsing slot: {slot_error}")
                    continue
            
            return slots
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
        logger.info(f"Getting user by phone {phone}")
        try:
            user_doc = self.collection.find_one({"phone": phone})
            if user_doc:
                user_doc["_id"] = str(user_doc["_id"])
                return User(**user_doc)
            return None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    def update_user_partial(self, user_id: str, update_data: Dict[str, Any]) -> bool:
        """Update user with partial fields"""
        logger.info(f"Updating user {user_id} with {update_data}")
        try:
            update_data["updated_at"] = datetime.utcnow()
            result = self.collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": update_data}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating user: {e}")
            return False
    
    def get_user_missing_fields(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user progress info with missing fields"""
        logger.info(f"Getting user missing fields for user {user_id}")
        try:
            user_doc = self.collection.find_one({"_id": ObjectId(user_id)})
            if not user_doc:
                return None
            
            missing_fields = []
            
            # Check if name is missing or is default format
            name = user_doc.get("name", "")
            if not name or name.startswith("User "):
                missing_fields.append("name")
            
            # Calculate completion percentage
            total_fields = 1  # Only name for now
            completed_fields = total_fields - len(missing_fields)
            completion_percentage = (completed_fields / total_fields) * 100
            
            # Determine current stage
            current_stage = "initial" if missing_fields else "completed"
            
            return {
                "user_id": str(user_doc["_id"]),
                "current_stage": current_stage,
                "missing_fields": missing_fields,
                "completion_percentage": completion_percentage
            }
        except Exception as e:
            print(f"Error getting buyer progress: {e}")
            return None
