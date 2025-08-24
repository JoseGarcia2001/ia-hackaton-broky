from typing import List, Optional, Dict, Any
from datetime import datetime
from pymongo.database import Database
from bson import ObjectId
from bson.errors import InvalidId

from ...models import Visit, VisitStatus


class VisitCRUD:
    """CRUD operations for Visit collection"""
    
    def __init__(self, db: Database):
        self.collection = db.visits

    def create_visit(self, visit_data: Dict[str, Any]) -> str:
        """Create a new visit with initial data"""
        visit_data["created_at"] = datetime.utcnow()
        visit_data["updated_at"] = datetime.utcnow()
        
        result = self.collection.insert_one(visit_data)
        return str(result.inserted_id)

    def get_visit_by_id(self, visit_id: str) -> Optional[Visit]:
        """Get a visit by ID"""
        try:
            obj_id = ObjectId(visit_id)
        except InvalidId:
            return None
        
        visit_doc = self.collection.find_one({"_id": obj_id})
        if visit_doc:
            visit_doc["_id"] = str(visit_doc["_id"])
            return Visit(**visit_doc)
        return None

    def get_visit_by_property_id_and_buyer_id(self, property_id: str, buyer_id: str) -> Optional[Visit]:
        """
        Get visit by property id and buyer id
        
        Args:
            property_id: Property ID
            buyer_id: Buyer ID
            
        Returns:
            Optional[Visit]: Visit object if found, None otherwise
        """
        try:
            visit_doc = self.collection.find_one({"property_id": property_id, "buyer_id": buyer_id})
            if visit_doc:
                visit_doc["_id"] = str(visit_doc["_id"])
                return Visit(**visit_doc)
            return None
        except Exception as e:
            print(f"Error getting visit: {e}")
            return None

    def update_visit(self, visit_id: str, update_data: Dict[str, Any]) -> bool:
        """Update visit with partial fields"""
        try:
            obj_id = ObjectId(visit_id)
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

    def get_visits_by_property_id(self, property_id: str) -> List[Visit]:
        """Get all visits for a specific property"""
        try:
            visit_docs = self.collection.find({"property_id": property_id}).sort("scheduled_at", 1)
            visits = []
            for doc in visit_docs:
                doc["_id"] = str(doc["_id"])
                visits.append(Visit(**doc))
            return visits
        except Exception as e:
            print(f"Error getting visits by property ID: {e}")
            return []

    def get_visits_by_buyer_id(self, buyer_id: str) -> List[Visit]:
        """Get all visits for a specific buyer"""
        try:
            visit_docs = self.collection.find({"buyer_id": buyer_id}).sort("scheduled_at", 1)
            visits = []
            for doc in visit_docs:
                doc["_id"] = str(doc["_id"])
                visits.append(Visit(**doc))
            return visits
        except Exception as e:
            print(f"Error getting visits by buyer ID: {e}")
            return []

    def get_visits_by_seller_id(self, seller_id: str) -> List[Visit]:
        """Get all visits for a specific seller"""
        try:
            visit_docs = self.collection.find({"seller_id": seller_id}).sort("scheduled_at", 1)
            visits = []
            for doc in visit_docs:
                doc["_id"] = str(doc["_id"])
                visits.append(Visit(**doc))
            return visits
        except Exception as e:
            print(f"Error getting visits by seller ID: {e}")
            return []

    def get_visits_by_seller_id_and_status(self, seller_id: str, status: VisitStatus) -> List[Visit]:
        """Get all visits for a specific seller with a specific status"""
        try:
            visit_docs = self.collection.find({
                "seller_id": seller_id,
                "status": status.value
            }).sort("scheduled_at", 1)
            visits = []
            for doc in visit_docs:
                doc["_id"] = str(doc["_id"])
                visits.append(Visit(**doc))
            return visits
        except Exception as e:
            print(f"Error getting visits by seller ID and status: {e}")
            return []

    def get_visits_by_status(self, status: VisitStatus) -> List[Visit]:
        """Get all visits with a specific status"""
        try:
            visit_docs = self.collection.find({"status": status.value}).sort("scheduled_at", 1)
            visits = []
            for doc in visit_docs:
                doc["_id"] = str(doc["_id"])
                visits.append(Visit(**doc))
            return visits
        except Exception as e:
            print(f"Error getting visits by status: {e}")
            return []

    def delete_visit(self, visit_id: str) -> bool:
        """Delete a visit by ID"""
        try:
            obj_id = ObjectId(visit_id)
        except InvalidId:
            return False
        
        result = self.collection.delete_one({"_id": obj_id})
        return result.deleted_count > 0

    def get_upcoming_visits(self, from_date: Optional[datetime] = None) -> List[Visit]:
        """Get all upcoming visits (confirmed status and future dates)"""
        if from_date is None:
            from_date = datetime.utcnow()
        
        try:
            visit_docs = self.collection.find({
                "status": VisitStatus.CONFIRMED.value,
                "scheduled_at": {"$gte": from_date}
            }).sort("scheduled_at", 1)
            
            visits = []
            for doc in visit_docs:
                doc["_id"] = str(doc["_id"])
                visits.append(Visit(**doc))
            return visits
        except Exception as e:
            print(f"Error getting upcoming visits: {e}")
            return []