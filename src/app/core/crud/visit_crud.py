from typing import List, Optional, Dict, Any
from pymongo.database import Database
from bson import ObjectId

from ...models import Visit, VisitStatus


class VisitCRUD:
    """CRUD operations for Visit collection"""
    
    def __init__(self, db: Database):
        self.collection = db.visits