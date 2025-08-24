from typing import Dict, Any
from datetime import datetime
from src.app.models.message import MessageSender, MessageType
from src.app.core.database import get_db
from src.app.core.crud.chat_crud import ChatCRUD
from src.app.core.crud.user_crud import UserCRUD
from src.app.core.crud.message_crud import MessageCRUD
from src.app.models.message import Message


def process_chat_message(message_data: Dict[str, Any]) -> Dict[str, Any]:
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
    db = get_db()
    chat_crud = ChatCRUD(db)
    user_crud = UserCRUD(db)
    message_crud = MessageCRUD(db)
    
    # Step 1: Get or create chat
    user_phone = message_data.get("from", "")
    chat = chat_crud.get_or_create_chat(user_phone)
    
    # Step 2: Get user type
    user_type = user_crud.get_user_type(user_phone)
    
    # Step 3: Store the message
    stored_message = message_crud.add_message(chat.id, message_data)
    
    # Step 4: Get full conversation history for agent context with sender info
    messages = message_crud.get_messages_by_chat(chat.id)
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


def get_user_conversation(user_phone: str) -> Dict[str, Any]:
    """
    Get all conversation history for a user
    
    Args:
        user_phone: User's phone number
        
    Returns:
        Dict containing chat info and all messages
    """
    db = get_db()
    chat_crud = ChatCRUD(db)
    message_crud = MessageCRUD(db)
    user_crud = UserCRUD(db)
    
    # Get chat for user
    chat = chat_crud.get_chat_by_user_phone(user_phone)
    
    if not chat:
        return {
            "chat": None,
            "messages": [],
            "user": None,
            "conversation_exists": False
        }
    
    # Get all messages for the chat
    messages = message_crud.get_messages_by_chat(chat.id)
    
    # Get user info
    user = user_crud.get_or_create_user(user_phone)
    
    return {
        "chat": chat,
        "messages": messages,
        "user": user,
        "conversation_exists": True,
        "message_count": len(messages)
    }


def save_agent_response(chat_id: str, agent_response: str) -> Message:
    """
    Save the agent's response to the chat
    
    Args:
        chat_id: ID of the chat to save the response to
        agent_response: The agent's response text
        
    Returns:
        Message: The saved message object
    """
    db = get_db()
    message_crud = MessageCRUD(db)
    
    # Create the agent response message data
    agent_message_data = {
        "type": "text",
        "content": {
            "text": agent_response,
            "type": "text"
        }
    }
    
    # Create message document for agent response
    
    message_doc = {
        "chat_id": chat_id,
        "sender": MessageSender.SYSTEM.value,
        "type": MessageType.TEXT.value,
        "content": agent_response,
        "timestamp": datetime.utcnow()
    }
    
    # Insert into MongoDB
    result = message_crud.collection.insert_one(message_doc)
    
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
