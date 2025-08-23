from typing import List, Optional, Dict, Any
from pymongo.database import Database
from bson import ObjectId

from ...models import Chat


class ChatCRUD:
    """CRUD operations for Chat collection"""
    
    def __init__(self, db: Database):
        self.collection = db.chats