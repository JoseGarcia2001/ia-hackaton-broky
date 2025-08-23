from typing import List, Optional, Dict, Any
from pymongo.database import Database
from bson import ObjectId

from ...models import Message, MessageType, MessageSender


class MessageCRUD:
    """CRUD operations for Message collection"""
    
    def __init__(self, db: Database):
        self.collection = db.messages