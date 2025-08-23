from typing import List, Optional, Dict, Any
from pymongo.database import Database
from bson import ObjectId
from datetime import datetime

from ...models import Chat


class ChatCRUD:
    """CRUD operations for Chat collection"""
    
    def __init__(self, db: Database):
        self.collection = db.chats
    
    def get_or_create_chat(self, user_phone: str) -> Chat:
        """
        Get existing chat or create new one for a user by phone number
        """
        # Try to find existing chat
        chat_doc = self.collection.find_one({"user_phone": user_phone})
        
        if chat_doc:
            # Return existing chat
            return Chat(
                id=str(chat_doc["_id"]),
                user_id=chat_doc["user_id"],
                created_at=chat_doc["created_at"],
                is_active=chat_doc.get("is_active", True)
            )
        else:
            # Create new chat
            chat_data = {
                "user_phone": user_phone,
                "user_id": f"user_{user_phone}",
                "created_at": datetime.utcnow(),
                "is_active": True
            }
            result = self.collection.insert_one(chat_data)
            
            return Chat(
                id=str(result.inserted_id),
                user_id=f"user_{user_phone}",
                created_at=chat_data["created_at"],
                is_active=True
            )
    
    def get_chat_by_user_phone(self, user_phone: str) -> Optional[Chat]:
        """
        Get existing chat by user phone number
        """
        chat_doc = self.collection.find_one({"user_phone": user_phone})
        
        if chat_doc:
            return Chat(
                id=str(chat_doc["_id"]),
                user_id=chat_doc["user_id"],
                created_at=chat_doc["created_at"],
                is_active=chat_doc.get("is_active", True)
            )
        
        return None