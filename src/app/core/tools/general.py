"""
Defines the tools for the general purposes
"""

from typing import Annotated, Dict, Any, Optional, List
from langchain.tools import tool
from langgraph.prebuilt import InjectedState

from src.app.core.crud.chat_crud import ChatCRUD
from src.app.core.crud.visit_crud import VisitCRUD
from src.app.core.crud.user_crud import UserCRUD
from src.app.core.database import get_db
from ...models.business_stage import SellerStage, BuyerStage
from ...models.user import AvailabilitySlot
from ...models.visit import VisitStatus
from ...services.stage_service import StageService
from ...services.user_service import UserService
from ...utils.logger import logger


@tool
def get_business_stage(user_type: str, state: Annotated[dict, InjectedState]) -> Dict[str, Any]:
    """
    Get the current business stage for a user (seller or buyer).

    Args:
        user_type: Type of user ("seller" or "buyer")
        state: Injected state containing chat_id

    Returns:
        Dictionary with stage information and status
    """
    logger.info(f"Getting business stage for user type {user_type}")
    try:
        chat_id = state.get("chat_id")

        stage_service = StageService()

        if user_type.lower() == "seller":
            stage = stage_service.get_seller_stage(chat_id)
            return {"success": True, "stage": stage.value}

        if user_type.lower() == "buyer":
            stage = stage_service.get_buyer_stage(chat_id)
            return {"success": True, "stage": stage.value if stage else None}
        return {
            "success": False,
            "stage": None,
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "stage": None,
        }


@tool
def save_availability(
    availability_slots: Annotated[List[AvailabilitySlot], "List of availability time slots"],
    state: Annotated[dict, InjectedState],
) -> Dict[str, Any]:
    """
    Herramienta útil para almacenar o actualizar el horario de disponibilidad del vendedor.

    Args:
        availability_slots: List of AvailabilitySlot objects with day_of_week, start_time, end_time, and optional description
        state: Injected state containing chat_id

    Returns:
        Dictionary with success status and message
    """
    logger.info("Saving availability")
    try:
        chat_id = state.get("chat_id")

        chat_crud = ChatCRUD(get_db())
        chat = chat_crud.get_chat_by_id(chat_id)
        if not chat:
            return {"success": False, "error": "No chat_id found in state", "message": "Error: Usuario no identificado"}

        user_service = UserService()
        success = user_service.add_availability(chat.user_id, availability_slots)

        if success:
            return {"success": True, "message": "Horario de disponibilidad almacenado correctamente"}

        return {"success": False, "message": "Error al almacenar el horario de disponibilidad"}

    except Exception as e:
        return {"success": False, "error": str(e), "message": "Error al procesar el horario de disponibilidad"}


@tool
def update_business_stage(
    stage: SellerStage | BuyerStage,
    user_type: Annotated[str, "Tipo de usuario (seller o buyer)"],
    state: Annotated[dict, InjectedState],
) -> Dict[str, Any]:
    """
    Herramienta útil para actualizar el estado del negocio
    """
    logger.info(f"Updating business stage for user type {user_type}")
    try:
        chat_id = state.get("chat_id")
        stage_service = StageService()

        if user_type.lower() == "seller":
            success = stage_service.update_seller_stage(chat_id, stage)
            return {
                "success": success,
                "stage": stage.value,
            }

        if user_type.lower() == "buyer":
            success = stage_service.update_buyer_stage(chat_id, stage)
            return {
                "success": success,
                "stage": stage.value,
            }

        return {
            "success": False,
            "stage": None,
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "stage": None,
        }


@tool
def get_last_buyer_from_visit(state: Annotated[dict, InjectedState]) -> Dict[str, Any]:
    """
    Herramienta útil para obtener información del último comprador que tuvo una visita.
    
    Returns:
        Dictionary with buyer information and visit status
    """
    logger.info("Getting last buyer from visit")
    try:
        chat_id = state.get("chat_id")
        
        # Get seller's user ID from chat
        chat_crud = ChatCRUD(get_db())
        chat = chat_crud.get_chat_by_id(chat_id)
        if not chat:
            return {"success": False, "error": "Chat no encontrado", "buyer_name": "comprador"}
        
        # Get visits for this seller
        visit_crud = VisitCRUD(get_db())
        visits = visit_crud.get_visits_by_seller_id(chat.user_id)
        
        if not visits:
            return {"success": False, "error": "No hay visitas programadas", "buyer_name": "comprador"}
        
        # Get the most recent visit
        latest_visit = sorted(visits, key=lambda x: x.scheduled_at, reverse=True)[0]
        
        # Get buyer information
        user_crud = UserCRUD(get_db())
        buyer = user_crud.get_user_by_id(latest_visit.buyer_id)
        
        buyer_name = buyer.name if buyer and buyer.name else "comprador"
        
        return {
            "success": True,
            "buyer_name": buyer_name,
            "visit_date": latest_visit.scheduled_at.strftime("%d/%m/%Y"),
            "visit_status": latest_visit.status.value
        }
        
    except Exception as e:
        logger.error(f"Error getting last buyer from visit: {e}")
        return {
            "success": False,
            "error": str(e),
            "buyer_name": "comprador"
        }