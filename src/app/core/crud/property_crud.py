from typing import List, Optional, Dict, Any
from pymongo.database import Database
from bson import ObjectId

from ...models import Property
from ...models.business_stage import SellerStage


class PropertyCRUD:
    """CRUD operations for Property collection"""
    
    def __init__(self, db: Database):
        self.collection = db.properties
    
    def get_property_stage(self, property_id: str) -> SellerStage:
        """Get the business stage of a property"""
        property_doc = self.collection.find_one({"_id": ObjectId(property_id)})
        if property_doc:
            return SellerStage(property_doc.get("business_stage", SellerStage.REGISTRATION))
        return SellerStage.REGISTRATION
    
    def update_property_stage(self, property_id: str, new_stage: SellerStage) -> bool:
        """Update the business stage of a property"""
        result = self.collection.update_one(
            {"_id": ObjectId(property_id)},
            {"$set": {"business_stage": new_stage.value}}
        )
        return result.modified_count > 0