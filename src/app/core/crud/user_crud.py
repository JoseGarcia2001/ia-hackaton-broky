from typing import List, Optional, Dict, Any
from pymongo.database import Database
from bson import ObjectId
from datetime import datetime

from ...models import User, UserRole


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
