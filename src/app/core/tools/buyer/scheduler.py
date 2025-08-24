"""
Defines the tools for the buyer scheduler agent
"""

from typing import Annotated, Optional, List, Dict, Any
from langchain.tools import tool
from langgraph.prebuilt import InjectedState
from ....services.chat_service import ChatService
from ....services.user_service import UserService, BuyerInfo, BuyerProgress
from ....services.visit_service import VisitService, VisitInfo
from ....services.property_service import PropertyService
from ....models.user import AvailabilitySlot
from ....models.visit import VisitStatus
from ....utils.logger import logger


@tool
def save_buyer_info(info: BuyerInfo, state: Annotated[dict, InjectedState]) -> str:
    """
    Herramienta útil para registrar la información del comprador.
    """
    logger.info("Saving buyer info")
    chat_id = state.get("chat_id")
    user_service = UserService()
    chat_service = ChatService()
    
    # Get user from chat to use as buyer
    user = chat_service.get_user_from_chat(chat_id)
    if not user:
        return "Error: No se pudo encontrar el usuario"
    
    # Update buyer info
    success = user_service.update_buyer_info(user.id, info)
    
    if success:
        return "Información del comprador registrada correctamente"
    else:
        return "Error: No se pudo guardar la información del comprador"


@tool
def get_remaining_buyer_info(state: Annotated[dict, InjectedState]) -> Optional[BuyerProgress]:
    """
    Herramienta útil para obtener la información que se necesita del posible comprador.
    """
    logger.info("Getting remaining buyer info")
    chat_id = state.get("chat_id")
    
    # Get user from chat service
    chat_service = ChatService()
    user = chat_service.get_user_from_chat(chat_id)
    
    if not user:
        # Return progress indicating all BuyerInfo fields are missing
        return BuyerProgress(
            user_id="",
            current_stage="initial",
            missing_fields=["name"],
            completion_percentage=0.0
        )
    
    user_service = UserService()
    return user_service.get_buyer_progress(user.id)


@tool
def get_seller_availability(state: Annotated[dict, InjectedState]) -> List[AvailabilitySlot]:
    """
    Herramienta útil para obtener la disponibilidad del vendedor.
    """
    logger.info("Getting seller availability")
    chat_id = state.get("chat_id")
    
    try:
        # Get the property associated with the chat
        chat_service = ChatService()
        property_service = PropertyService()
        
        chat = chat_service.get_chat_by_id(chat_id)
        if not chat or not chat.property_id:
            logger.warning(f"No chat_id found for chat_id: {chat_id}")
            return []
        
        property_obj = property_service.get_property_full_info(chat.property_id)
        
        if not property_obj:
            logger.warning(f"No property found for property_id: {chat.property_id}")
            return []
        
        # Get property availability through visit service
        visit_service = VisitService()
        availability_slots = visit_service.get_property_availability(property_obj.id)
        
        return availability_slots
        
    except Exception as e:
        logger.error(f"Error getting seller availability: {e}")
        return []


@tool
def save_visit_info(requested_slot: AvailabilitySlot, state: Annotated[dict, InjectedState]) -> Dict[str, Any]:
    """
    Herramienta útil para registrar la información de la visita.
    """
    logger.info("Saving visit info")
    try:
        chat_id = state.get("chat_id")
        visit_service = VisitService()
        
        result = visit_service.attempt_visit_creation(chat_id, requested_slot)
        return result
        
    except Exception as e:
        logger.error(f"Error saving visit info: {e}")
        return {
            "success": False, 
            "message": "Error interno del sistema", 
            "available_slots": []
        }


@tool
def notify_seller(state: Annotated[dict, InjectedState]) -> str:
    """
    Herramienta útil para notificar al vendedor sobre la visita.
    """
    logger.info("Notifying seller")
    from src.app.services.infobip_service import InfobipService

    chat_id = state.get("chat_id")
    chat_service = ChatService()
    user = chat_service.get_user_from_chat(chat_id)
    property = chat_service.get_property_from_buyer_chat_id(chat_id)

    if not property or not user:
        return "No se encontró la propiedad o el usuario"

    # Obtener la visita usando el service
    visit_service = VisitService()
    visit = visit_service.get_visit_by_property_and_buyer(property.id, user.id)

    if not visit:
        return "No se encontró la visita"
    
    # Obtener datos formateados para la plantilla usando el service
    template_data = visit_service.get_visit_template_data(visit)
    
    # Enviar plantilla de la cita con datos reales
    InfobipService().send_template_message(
        to=user.phone,
        template_name="schedule_buyer_notification",
        language="es",
        template_data={
            "placeholders": [
                template_data.seller_name,
                template_data.buyer_name,
                template_data.visit_date,
                template_data.visit_time,
            ]
        }
    )

    return "Notificación enviada correctamente"
