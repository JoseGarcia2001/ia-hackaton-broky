"""
Defines the tools for the buyer scheduler agent
"""

from typing import Annotated, Dict, Any, Optional
from langchain.tools import tool
from langgraph.prebuilt import InjectedState
from src.app.services.chat_service import ChatService
from src.app.services.visit_service import VisitService
from src.app.services.visit_service import VisitTemplateData


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

    return {
        "name": None
    }


@tool
def get_seller_availability(state: Annotated[dict, InjectedState]) -> str:
    """
    Herramienta útil para obtener la disponibilidad del vendedor.
    """

    return "El vendedor está disponible los sábados de 2 a 4"

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
