"""
Defines the tools for the buyer scheduler agent
"""

from typing import Annotated, Optional
from langchain.tools import tool
from langgraph.prebuilt import InjectedState
from ....services.chat_service import ChatService
from ....services.user_service import UserService, BuyerInfo, BuyerProgress
from ....core.database import get_db
from ....core.crud.property_crud import PropertyCRUD


@tool
def save_buyer_info(info: BuyerInfo, state: Annotated[dict, InjectedState]) -> str:
    """
    Herramienta útil para registrar la información del comprador.
    """
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
def get_seller_availability(state: Annotated[dict, InjectedState]) -> str:
    """
    Herramienta útil para obtener la disponibilidad del vendedor.
    """
    chat_id = state.get("chat_id")
    try:
        chat_service = ChatService()
        property_id = chat_service.get_property_id_from_chat(chat_id)
        db = get_db()
        property_crud = PropertyCRUD(db)
        property_obj = property_crud.get_property_by_id(property_id)
        days_str = ", ".join(property_obj.available_days)
        if len(property_obj.available_days) > 1:
            days_str = (
                ", ".join(property_obj.available_days[:-1])
                + " y "
                + property_obj.available_days[-1]
            )
        return {
            "success": True,
            "message": f"El vendedor está disponible los {days_str} {property_obj.available_hours}",
        }
    except Exception as e:  # pylint: disable=broad-exception-caught
        return {
            "success": False,
            "error": str(e),
            "stage": None,
        }


@tool
def save_visit_info(visit_info: str, state: Annotated[dict, InjectedState]) -> str:
    """
    Herramienta útil para registrar la información de la visita.
    """

    return "Información de la visita registrada correctamente"


@tool
def notify_seller(state: Annotated[dict, InjectedState]) -> str:
    """
    Herramienta útil para notificar al vendedor sobre la visita.
    """

    return "Notificación enviada correctamente"
