from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime

from ..core.crud.visit_crud import VisitCRUD
from ..core.crud.user_crud import UserCRUD
from ..core.crud.property_crud import PropertyCRUD
from ..core.crud.chat_crud import ChatCRUD
from ..core.database import get_db
from ..models.visit import Visit, VisitStatus
from ..models.user import AvailabilitySlot


class VisitInfo(BaseModel):
    """
    Información mínima para programar una visita.
    """
    property_id: str = Field(description="ID de la propiedad")
    buyer_id: str = Field(description="ID del comprador")
    seller_id: str = Field(description="ID del vendedor")
    scheduled_at: datetime = Field(description="Fecha y hora programada para la visita")
    notes: Optional[str] = Field(None, description="Notas adicionales")


class VisitTemplateData(BaseModel):
    """Datos formateados para plantillas de notificación"""
    seller_name: str
    buyer_name: str
    visit_date: str
    visit_time: str
    visit_status: Optional[str] = None
    visit_id: Optional[str] = None


class VisitService:
    """Service layer for visit operations"""
    
    def __init__(self):
        db = get_db()
        self.visit_crud = VisitCRUD(db)
        self.user_crud = UserCRUD(db)
        self.property_crud = PropertyCRUD(db)
        self.chat_crud = ChatCRUD(db)
    
    def get_visit_by_property_and_buyer(self, property_id: str, buyer_id: str) -> Optional[Visit]:
        """Get visit by property and buyer IDs"""
        return self.visit_crud.get_visit_by_property_id_and_buyer_id(property_id, buyer_id)

    def format_date_spanish(self, date: datetime) -> str:
        """Formatear fecha en español"""
        months = {
            1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
            5: "mayo", 6: "junio", 7: "julio", 8: "agosto", 
            9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
        }
        
        day = date.day
        month = months[date.month]
        return f"{day} de {month}"

    def format_time_spanish(self, date: datetime) -> str:
        """Formatear hora en español (formato 24 horas)"""
        return date.strftime("%H:%M")

    def get_visit_template_data(self, visit: Visit) -> VisitTemplateData:
        """
        Obtener datos de la visita para plantillas de notificación
        
        Args:
            visit: Objeto Visit con la información de la visita
            
        Returns:
            VisitTemplateData con los datos formateados para la plantilla
        """
        try:
            # Obtener información del vendedor
            seller = self.user_crud.get_user_by_id(visit.seller_id)
            seller_name = seller.name if seller else "Vendedor"
            
            # Obtener información del comprador
            buyer = self.user_crud.get_user_by_id(visit.buyer_id)
            buyer_name = buyer.name if buyer else "Comprador"
            
            # Formatear fecha y hora
            visit_date = self.format_date_spanish(visit.scheduled_at)
            visit_time = self.format_time_spanish(visit.scheduled_at)
            
            return VisitTemplateData(
                seller_name=seller_name,
                buyer_name=buyer_name,
                visit_date=visit_date,
                visit_time=visit_time,
                visit_status=visit.status.value,
                visit_id=visit.id
            )
        except Exception as e:
            print(f"Error getting visit template data: {e}")
            # Datos por defecto en caso de error
            return VisitTemplateData(
                seller_name="", 
                buyer_name="",
                visit_date="",
                visit_time="",
                visit_status=""
            )
    

    async def schedule_visit(self, info: VisitInfo) -> Optional[Visit]:
        """Schedule a new visit and return the full visit object"""
        # Convert VisitInfo to visit data
        visit_data = {
            "property_id": info.property_id,
            "buyer_id": info.buyer_id,
            "seller_id": info.seller_id,
            "scheduled_at": info.scheduled_at,
            "status": VisitStatus.REQUESTED,
            "notes": info.notes,
            "created_at": datetime.utcnow()
        }
        
        visit_id = self.visit_crud.create_visit(visit_data)
        return self.visit_crud.get_visit_by_id(visit_id)

    
    async def get_visit_by_id(self, visit_id: str) -> Optional[Visit]:
        """Get visit by ID"""
        return self.visit_crud.get_visit_by_id(visit_id)
    
    async def update_visit_status(self, visit_id: str, status: VisitStatus, notes: Optional[str] = None) -> bool:
        """Update visit status and optionally add notes"""
        update_data = {
            "status": status,
            "updated_at": datetime.utcnow()
        }
        
        if notes:
            update_data["notes"] = notes
        
        return self.visit_crud.update_visit(visit_id, update_data)

    def get_property_availability(self, property_id: str) -> List[AvailabilitySlot]:
        """
        Get availability slots for a property by getting the property owner's availability
        
        Args:
            property_id: ID of the property
            
        Returns:
            List[AvailabilitySlot]: List of availability slots from the property owner
        """
        try:
            # Get property to find the owner
            property_obj = self.property_crud.get_property_by_id(property_id)
            if not property_obj or not property_obj.owner_id:
                return []
            
            # Get owner's availability
            return self.user_crud.get_user_availability(property_obj.owner_id)
            
        except Exception as e:
            print(f"Error getting property availability: {e}")
            return []
    
    
    def check_seller_availability_conflict(self, seller_id: str, start_time: datetime, end_time: datetime) -> bool:
        """
        Check if the requested slot conflicts with seller's availability slots
        
        Args:
            seller_id: ID of the seller
            start_time: Start datetime of the requested visit
            end_time: End datetime of the requested visit
            
        Returns:
            bool: True if there are conflicts (seller is busy), False if available
        """
        try:
            # Use user CRUD to check availability directly
            return not self.user_crud.check_availability(
                seller_id, 
                start_time, 
                end_time
            )
            
        except Exception as e:
            print(f"Error checking seller availability: {e}")
            return True  # Return True (conflict) on error to be safe
    
    def attempt_visit_creation(self, chat_id: str, start_time: datetime, end_time: datetime, description: Optional[str] = None) -> dict:
        """
        Attempt to create a visit after checking availability conflicts
        
        Args:
            chat_id: Chat ID to get property and buyer info
            start_time: Start datetime of the requested visit
            end_time: End datetime of the requested visit
            description: Optional description for the visit
            
        Returns:
            dict: Success/failure with message and available_slots if needed
        """
        try:
            # Get chat using CRUD
            chat = self.chat_crud.get_chat_by_id(chat_id)
            if not chat:
                return {"success": False, "message": "No se encontró el chat", "available_slots": []}
            
            # Get property from chat property_id
            if not chat.property_id:
                return {"success": False, "message": "No se encontró la propiedad", "available_slots": []}
            
            property_obj = self.property_crud.get_property_by_id(chat.property_id)
            if not property_obj:
                return {"success": False, "message": "No se encontró la propiedad", "available_slots": []}
            
            # Get buyer from chat using user_phone
            if not chat.user_phone:
                return {"success": False, "message": "No se encontró el comprador", "available_slots": []}
                
            buyer = self.user_crud.get_user_by_phone(chat.user_phone)
            if not buyer:
                return {"success": False, "message": "No se encontró el comprador", "available_slots": []}
            
            # Check seller availability conflict
            has_conflict = self.check_seller_availability_conflict(property_obj.owner_id, start_time, end_time)
            
            if has_conflict:
                # Get available slots to return to user
                available_slots = self.get_property_availability(property_obj.id)
                return {
                    "success": False, 
                    "message": "Horario no disponible", 
                    "available_slots": available_slots
                }
            
            # No conflicts - create the visit
            visit_info = VisitInfo(
                property_id=property_obj.id,
                buyer_id=buyer.id,
                seller_id=property_obj.owner_id,
                scheduled_at=start_time,
                notes=description
            )
            
            # Create visit data with CONFIRMED status
            visit_data = {
                "property_id": visit_info.property_id,
                "buyer_id": visit_info.buyer_id,
                "seller_id": visit_info.seller_id,
                "scheduled_at": visit_info.scheduled_at,
                "status": VisitStatus.CONFIRMED,
                "notes": visit_info.notes,
                "created_at": datetime.utcnow()
            }
            
            visit_id = self.visit_crud.create_visit(visit_data)
            visit = self.visit_crud.get_visit_by_id(visit_id)
            
            if visit:
                # Add the confirmed visit slot to seller's availability
                visit_slot = AvailabilitySlot(
                    day_of_week=start_time.weekday(),
                    start_time=start_time.time(),
                    end_time=end_time.time(),
                    description=f"Visita confirmada - {buyer.name if buyer.name else 'Comprador'}"
                )
                
                # Use user CRUD to add the slot directly to seller's availability
                slot_added = self.user_crud.add_availability(property_obj.owner_id, [visit_slot])
                
                if not slot_added:
                    print(f"Warning: Could not add visit slot to seller's availability for visit {visit.id}")
                
                return {
                    "success": True, 
                    "message": "Visita confirmada correctamente", 
                    "visit_id": visit.id
                }
            else:
                return {
                    "success": False, 
                    "message": "Error al crear la visita", 
                    "available_slots": []
                }
                
        except Exception as e:
            print(f"Error attempting visit creation: {e}")
            return {
                "success": False, 
                "message": "Error interno del sistema", 
                "available_slots": []
            }
