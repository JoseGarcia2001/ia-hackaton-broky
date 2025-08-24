from typing import Optional
from ..core.database import get_db
from ..core.crud.property_crud import PropertyCRUD
from ..core.crud.chat_crud import ChatCRUD
from ..models.business_stage import SellerStage, BuyerStage


class StageService:
    """Service for managing business stages"""
    
    def __init__(self):
        self.db = get_db()
        self.property_crud = PropertyCRUD(self.db)
        self.chat_crud = ChatCRUD(self.db)
    
    def get_seller_stage(self, chat_id: str) -> SellerStage:
        """Get seller business stage from chat context"""
        # Get chat to find property_id
        chat_doc = self.db.chats.find_one({"_id": chat_id})
        if not chat_doc or not chat_doc.get("property_id"):
            return SellerStage.REGISTRATION
        
        # Get property stage
        return self.property_crud.get_property_stage(chat_doc["property_id"])
    
    def get_buyer_stage(self, chat_id: str) -> Optional[BuyerStage]:
        """Get buyer business stage from chat"""
        return self.chat_crud.get_chat_stage(chat_id)
    
    def update_seller_stage(self, chat_id: str, new_stage: SellerStage) -> bool:
        """Update seller business stage via property"""
        # Get chat to find property_id
        chat_doc = self.db.chats.find_one({"_id": chat_id})
        if not chat_doc or not chat_doc.get("property_id"):
            return False
        
        return self.property_crud.update_property_stage(chat_doc["property_id"], new_stage)
    
    def update_buyer_stage(self, chat_id: str, new_stage: BuyerStage) -> bool:
        """Update buyer business stage in chat"""
        return self.chat_crud.update_chat_stage(chat_id, new_stage)