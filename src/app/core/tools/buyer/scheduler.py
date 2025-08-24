"""
Defines the tools for the buyer scheduler agent
"""

from typing import Annotated
from langchain.tools import tool
from langgraph.prebuilt import InjectedState
from ....services.chat_service import ChatService
from ....core.database import get_db
from ....core.crud.property_crud import PropertyCRUD


@tool
def save_buyer_info(buyer_info: str, state: Annotated[dict, InjectedState]) -> str:
    """
    Herramienta útil para registrar la información del comprador.
    """

    return "Información del comprador registrada correctamente"


@tool
def get_remaining_buyer_info(state: Annotated[dict, InjectedState]) -> str:
    """
    Herramienta útil para obtener la información que se necesita del posible comprador.
    """

    return {"name": None}


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
