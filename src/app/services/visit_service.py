from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

from ..core.crud.visit_crud import VisitCRUD
from ..core.crud.user_crud import UserCRUD
from ..core.database import get_db
from ..models.visit import Visit, VisitStatus


class VisitInfo(BaseModel):
    """
    Información mínima para programar una visita.
    """
    property_id: str = Field(description="ID de la propiedad")
    buyer_id: str = Field(description="ID del comprador")
    seller_id: str = Field(description="ID del vendedor")
    scheduled_at: datetime = Field(description="Fecha y hora programada para la visita")
    notes: Optional[str] = Field(None, description="Notas adicionales sobre la visita")


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
