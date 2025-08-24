from typing import List, Optional, Dict, Any
from pymongo.database import Database
from bson import ObjectId
from datetime import datetime

from ...models import Chat
from ...models.business_stage import BuyerStage


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
                user_phone=chat_doc.get("user_phone"),
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
                user_phone=user_phone,
                created_at=chat_data["created_at"],
                is_active=True
            )
    
    def update_chat_user_id(self, chat_id: str, user_id: str) -> bool:
        """
        Update the user_id of a chat
        
        Args:
            chat_id: Chat ID
            user_id: New user ID
            
        Returns:
            bool: True if updated successfully, False otherwise
        """
        try:
            result = self.collection.update_one(
                {"_id": ObjectId(chat_id)},
                {"$set": {"user_id": user_id}}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating chat user_id: {e}")
            return False
    
    def get_chat_by_user_phone(self, user_phone: str) -> Optional[Chat]:
        """
        Get existing chat by user phone number
        """
        chat_doc = self.collection.find_one({"user_phone": user_phone})
        
        if chat_doc:
            return Chat(
                id=str(chat_doc["_id"]),
                user_id=chat_doc["user_id"],
                user_phone=chat_doc.get("user_phone"),
                created_at=chat_doc["created_at"],
                is_active=chat_doc.get("is_active", True)
            )
        
        return None
    
    def get_chat_stage(self, chat_id: str) -> Optional[BuyerStage]:
        """Get the business stage of a chat"""
        chat_doc = self.collection.find_one({"_id": ObjectId(chat_id)})
        if chat_doc and "business_stage" in chat_doc:
            return BuyerStage(chat_doc["business_stage"])
        return None
    
    def update_chat_stage(self, chat_id: str, new_stage: BuyerStage) -> bool:
        """Update the business stage of a chat"""
        result = self.collection.update_one(
            {"_id": ObjectId(chat_id)},
            {"$set": {"business_stage": new_stage.value}}
        )
        return result.modified_count > 0
    
    def get_chat_by_id(self, chat_id: str) -> Optional[Chat]:
        """
        Get chat by ID
        
        Args:
            chat_id: Chat ID
            
        Returns:
            Optional[Chat]: Chat object if found, None otherwise
        """
        try:
            chat_doc = self.collection.find_one({"_id": ObjectId(chat_id)})
            
            if chat_doc:
                return Chat(
                    id=str(chat_doc["_id"]),
                    user_id=chat_doc["user_id"],
                    user_phone=chat_doc.get("user_phone"),
                    created_at=chat_doc["created_at"],
                    is_active=chat_doc.get("is_active", True)
                )
            
            return None
        except Exception as e:
            print(f"Error getting chat by id: {e}")
            return None