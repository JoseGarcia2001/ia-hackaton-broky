from typing import List, Optional, Dict, Any
from datetime import datetime
from pymongo.database import Database
from bson import ObjectId
from bson.errors import InvalidId

from ...models import Property
from ...models.business_stage import SellerStage
from ...utils.logger import logger


class PropertyCRUD:
    """CRUD operations for Property collection"""
    
    def __init__(self, db: Database):
        self.collection = db.properties
    
    def create_property(self, property_data: Dict[str, Any]) -> str:
        """Create a new property with initial data"""
        logger.info(f"Creating property with data {property_data}")
        property_data["created_at"] = datetime.utcnow()
        property_data["updated_at"] = datetime.utcnow()
        
        result = self.collection.insert_one(property_data)
        return str(result.inserted_id)
    
    def get_property_id_by_address(self, address: str) -> Optional[str]:
        """Get property ID by address"""
        logger.info(f"Getting property ID by address {address}")
        property_doc = self.collection.find_one({"address": address}, {"_id": 1})
        if property_doc:
            return str(property_doc["_id"])
        return None
    
    def get_property_by_id(self, property_id: str) -> Optional[Property]:
        """Get a property by ID"""
        logger.info(f"Getting property by ID {property_id}")
        try:
            obj_id = ObjectId(property_id)
        except InvalidId:
            return None
        
        property_doc = self.collection.find_one({"_id": obj_id})
        if property_doc:
            property_doc["_id"] = str(property_doc["_id"])
            return Property(**property_doc)
        return None
    
    def get_property_by_address(self, address: str) -> Optional[Property]:
        """Get a property by address"""
        logger.info(f"Getting property by address {address}")
        property_doc = self.collection.find_one({"address": address})
        if property_doc:
            property_doc["_id"] = str(property_doc["_id"])
            return Property(**property_doc)
        return None
    
    def update_property_partial(self, property_id: str, update_data: Dict[str, Any]) -> bool:
        """Update property with partial fields"""
        logger.info(f"Updating property {property_id} with {update_data}")
        try:
            obj_id = ObjectId(property_id)
        except InvalidId:
            return False
        
        if not update_data:
            return False
        
        # Filter out None values and prepare update data
        filtered_update = {k: v for k, v in update_data.items() if v is not None}
        
        if not filtered_update:
            return False
        
        # Add updated_at timestamp
        filtered_update["updated_at"] = datetime.utcnow()
        
        result = self.collection.update_one(
            {"_id": obj_id},
            {"$set": filtered_update}
        )
        
        return result.modified_count > 0
    
    def get_property_missing_fields(self, property_id: str) -> Optional[Dict[str, Any]]:
        """Get property missing fields for progress tracking"""
        logger.info(f"Getting property missing fields for property {property_id}")
        property_obj = self.get_property_by_id(property_id)
        if not property_obj:
            return None
        
        missing_fields = []
        
        # Check required fields that might be missing or empty
        if not property_obj.address or property_obj.address.strip() == "":
            missing_fields.append("address")
        
        if not property_obj.type or property_obj.type.strip() == "":
            missing_fields.append("type")
        
        if property_obj.value <= 0:
            missing_fields.append("value")
        
        if not property_obj.description or property_obj.description.strip() == "":
            missing_fields.append("description")
        
        if len(property_obj.images) < 3:
            missing_fields.append("images")
        
        return {
            "property_id": property_id,
            "current_stage": property_obj.business_stage,
            "missing_fields": missing_fields,
            "completion_percentage": round((5 - len(missing_fields)) / 5 * 100, 2)
        }
    
    def get_property_stage(self, property_id: str) -> SellerStage:
        """Get the business stage of a property"""
        logger.info(f"Getting property stage for property {property_id}")
        property_doc = self.collection.find_one({"_id": ObjectId(property_id)})
        if property_doc:
            return SellerStage(property_doc.get("business_stage", SellerStage.REGISTRATION))
        return SellerStage.REGISTRATION
    
    def update_property_stage(self, property_id: str, new_stage: SellerStage) -> bool:
        """Update the business stage of a property"""
        logger.info(f"Updating property stage for property {property_id} to {new_stage}")
        result = self.collection.update_one(
            {"_id": ObjectId(property_id)},
            {"$set": {"business_stage": new_stage.value}}
        )
        return result.modified_count > 0