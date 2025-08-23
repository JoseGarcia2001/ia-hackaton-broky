from typing import List, Optional, Dict, Any
from pymongo.database import Database
from bson import ObjectId
from datetime import datetime

from ...models import Message, MessageType, MessageSender


class MessageCRUD:
    """CRUD operations for Message collection"""
    
    def __init__(self, db: Database):
        self.collection = db.messages
    
    def add_message(self, chat_id: str, processed_message: Dict[str, Any]) -> Message:
        """
        Add message to MongoDB
        """
        # Determine message type
        content_type = processed_message.get("type", "text").lower()
        if content_type == "text":
            message_type = MessageType.TEXT
            content = processed_message.get("content", {}).get("text", "")
        elif content_type == "image":
            message_type = MessageType.IMAGE
            content = processed_message.get("content", {}).get("url", "")
        elif content_type == "audio":
            message_type = MessageType.AUDIO
            content = processed_message.get("content", {}).get("url", "")
        else:
            message_type = MessageType.TEXT
            content = str(processed_message.get("content", {}))
        
        # Create message document
        message_doc = {
            "chat_id": chat_id,
            "sender": MessageSender.USER.value,
            "type": message_type.value,
            "content": content,
            "timestamp": datetime.utcnow()
        }
        
        # Insert into MongoDB
        result = self.collection.insert_one(message_doc)
        
        # Return Message object with generated ID
        message = Message(
            id=str(result.inserted_id),
            chat_id=chat_id,
            sender=MessageSender.USER,
            type=message_type,
            content=content,
            timestamp=message_doc["timestamp"]
        )
        
        return message
    
    def get_messages_by_chat(self, chat_id: str) -> List[Message]:
        """
        Get all messages for a specific chat
        """
        # Query messages from MongoDB
        message_docs = self.collection.find(
            {"chat_id": chat_id}
        ).sort("timestamp", 1)  # Sort by timestamp ascending
        
        # Convert documents to Message objects
        messages = []
        for doc in message_docs:
            message = Message(
                id=str(doc["_id"]),
                chat_id=doc["chat_id"],
                sender=MessageSender(doc["sender"]),
                type=MessageType(doc["type"]),
                content=doc["content"],
                timestamp=doc["timestamp"]
            )
            messages.append(message)
        
        return messages