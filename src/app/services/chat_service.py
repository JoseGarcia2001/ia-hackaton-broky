from typing import Dict, Any, Optional
from datetime import datetime
from ..models.user import User
from ..models.property import Property
from ..models.message import MessageSender, MessageType, Message
from ..core.database import get_db
from ..core.crud.chat_crud import ChatCRUD
from ..core.crud.user_crud import UserCRUD
from ..core.crud.message_crud import MessageCRUD

class ChatService:
    """Service layer for chat operations"""
    
    def __init__(self):
        db = get_db()
        self.chat_crud = ChatCRUD(db)
        self.user_crud = UserCRUD(db)
        self.message_crud = MessageCRUD(db)
    
    async def process_chat_message(self, message_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process chat message through the 5 steps:
        1. Create chat if not existent
        2. Get user type  
        3. Process message type (already done by infobip_service)
        4. Store the message
        5. Return structured data with full context for agent processing
        
        Args:
            message_data: Processed message data from Infobip
            Example: {
                'id': 'f1e6b8c3-1d2e-4c3a-9f0e-123456789abc',
                'from': '34600123456',
                'to': '447908680611', 
                'received_at': '2025-08-23T20:09:54.000+0000',
                'type': 'text',
                'content': {'text': 'Oeee', 'type': 'text'},
                'is_valid': True
            }
            
        Returns:
            Dict containing user_type, latest message, and conversation history
        """
        # Step 1: Get or create chat
        user_phone = message_data.get("from", "")
        chat = self.chat_crud.get_or_create_chat(user_phone)
        
        # Step 2: Get user type
        user_type = self.user_crud.get_user_type(user_phone)
        
        # Step 3: Store the message
        stored_message = self.message_crud.add_message(chat.id, message_data)
        
        # Step 4: Get full conversation history for agent context with sender info
        messages = self.message_crud.get_messages_by_chat(chat.id)
        conversation_history = [
            {
                "content": msg.content,
                "sender": msg.sender.value,
                "type": msg.type.value,
            }
            for msg in messages
        ]

        
        return {
            "user_type": user_type,
            "latest_message": stored_message.content,
            "conversation_history": conversation_history,
            "chat_id": chat.id
        }

    
    async def get_user_conversation(self, user_phone: str) -> Dict[str, Any]:
        """
        Get all conversation history for a user
        
        Args:
            user_phone: User's phone number
            
        Returns:
            Dict containing chat info and all messages
        """
        # Get chat for user
        chat = self.chat_crud.get_chat_by_user_phone(user_phone)
        
        if not chat:
            return {
                "chat": None,
                "messages": [],
                "user": None,
                "conversation_exists": False
            }
        
        # Get all messages for the chat
        messages = self.message_crud.get_messages_by_chat(chat.id)
        
        # Get user info
        user = self.user_crud.get_or_create_user(user_phone)
        
        return {
            "chat": chat,
            "messages": messages,
            "user": user,
            "conversation_exists": True,
            "message_count": len(messages)
        }

    
    async def save_agent_response(self, chat_id: str, agent_response: str) -> Message:
        """
        Save the agent's response to the chat
        
        Args:
            chat_id: ID of the chat to save the response to
            agent_response: The agent's response text
            
        Returns:
            Message: The saved message object
        """
        # Create message document for agent response
        message_doc = {
            "chat_id": chat_id,
            "sender": MessageSender.SYSTEM.value,
            "type": MessageType.TEXT.value,
            "content": agent_response,
            "timestamp": datetime.utcnow()
        }
        
        # Insert into MongoDB
        result = self.message_crud.collection.insert_one(message_doc)
        
        # Return Message object with generated ID
        message = Message(
            id=str(result.inserted_id),
            chat_id=chat_id,
            sender=MessageSender.SYSTEM,
            type=MessageType.TEXT,
            content=agent_response,
            timestamp=message_doc["timestamp"]
        )
        
        return message


    
    async def get_property_id_from_chat(self, chat_id: str):
        """
        Get property ID associated with a chat by finding property owned by the chat's user
        
        Args:
            chat_id: ID of the chat
            
        Returns:
            Property ID string or None if not found
        """
        from ..core.crud.property_crud import PropertyCRUD
        
        db = get_db()
        property_crud = PropertyCRUD(db)
        
        # Get user from chat
        chat = self.chat_crud.get_chat_by_id(chat_id)
        if not chat or not chat.user_id:
            return None
        
        user = self.user_crud.get_user_by_id(chat.user_id)
        if not user:
            return None
        
        # Find property owned by this user (assuming one property per user for now)
        properties = property_crud.collection.find({"owner_id": user.id}).limit(1)
        for prop in properties:
            return str(prop["_id"])
        
        return None
    
    async def get_user_from_chat(self, chat_id: str) -> Optional[User]:
        """
        Get user associated with a chat
        
        Args:
            chat_id: ID of the chat
            
        Returns:
            Optional[User]: User object if found, None otherwise
        """
        # Get chat
        chat = self.chat_crud.get_chat_by_id(chat_id)
        if not chat or not chat.user_phone:
            return None
        
        # Get user by phone
        return self.user_crud.get_user_by_phone(chat.user_phone)

    def get_property_from_buyer_chat_id(self, chat_id: str) -> Optional[Property]:
        """
        Get property associated with a chat
        
        Args:
            chat_id: ID of the chat
            
        Returns:
            Optional[Property]: Property object if found, None otherwise
        """
        from ..core.crud.property_crud import PropertyCRUD

        chat = self.chat_crud.get_chat_by_id(chat_id)
        if not chat or not chat.property_id:
            return None       
        
        db = get_db()
        property_crud = PropertyCRUD(db)
        property = property_crud.get_property_by_id(chat.property_id)
        if not property:
            return None

        return property
