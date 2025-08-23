from typing import List, Optional, Dict, Any
from pymongo.database import Database
from bson import ObjectId

from ...models import User, UserRole


class UserCRUD:
    """CRUD operations for User collection"""
    
    def __init__(self, db: Database):
        self.collection = db.users