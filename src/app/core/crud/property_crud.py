from typing import List, Optional, Dict, Any
from pymongo.database import Database
from bson import ObjectId

from ...models import Property


class PropertyCRUD:
    """CRUD operations for Property collection"""
    
    def __init__(self, db: Database):
        self.collection = db.properties