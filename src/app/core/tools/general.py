"""
Defines the tools for the general purposes
"""

from typing import Annotated, Dict, Any, Optional, List
from langchain.tools import tool
from langgraph.prebuilt import InjectedState
from ...models.business_stage import SellerStage, BuyerStage
from ...models.user import AvailabilitySlot
from ...services.stage_service import StageService
from ...services.user_service import UserService


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
    try:
        chat_id = state.get("chat_id")
        
        stage_service = StageService()
        
        if user_type.lower() == "seller":
            stage = stage_service.get_seller_stage(chat_id)
            return {
                "success": True,
                "stage": stage.value 
            }

        if user_type.lower() == "buyer":
            stage = stage_service.get_buyer_stage(chat_id)
            return {
                "success": True,
                "stage": stage.value if stage else None
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
def save_availability(availability_slots: Annotated[List[AvailabilitySlot], "List of availability time slots"], state: Annotated[dict, InjectedState]) -> Dict[str, Any]:
    """
    Herramienta útil para almacenar o actualizar el horario de disponibilidad del vendedor.
    
    Args:
        availability_slots: List of AvailabilitySlot objects with start_time, end_time, and optional description
        state: Injected state containing chat_id
    
    Returns:
        Dictionary with success status and message
    """
    try:
        chat_id = state.get("chat_id")
        if not chat_id:
            return {
                "success": False,
                "error": "No chat_id found in state",
                "message": "Error: Usuario no identificado"
            }
        
        user_service = UserService()
        success = user_service.add_availability(chat_id, availability_slots)
        
        if success:
            return {
                "success": True,
                "message": "Horario de disponibilidad almacenado correctamente"
            }

        return {
            "success": False,
            "message": "Error al almacenar el horario de disponibilidad"
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Error al procesar el horario de disponibilidad"
        }


@tool
def update_business_stage(
    stage: SellerStage | BuyerStage, user_type: str, state: Annotated[dict, InjectedState]
) -> Dict[str, Any]:
    """
    Update the business stage for a user (seller or buyer).
    
    Args:
        stage: New business stage (SellerStage or BuyerStage)
        user_type: Type of user ("seller" or "buyer")  
        state: Injected state containing chat_id
    
    Returns:
        Dictionary with update result and stage information
    """
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
