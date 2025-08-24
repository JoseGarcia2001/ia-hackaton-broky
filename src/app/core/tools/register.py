"""
Defines the tools for the register agent.
"""

from typing import Annotated, Optional, Dict, Any
from langchain.tools import tool
from pydantic import BaseModel, Field
from langgraph.prebuilt import InjectedState



from ...services.property_service import PropertyService, PropertyInfo, PropertyProgress

from ...services.chat_service import ChatService

from ...models.property import Property
from ...models.user import User

from ...utils.logger import logger


@tool
def get_user_info(state: Annotated[dict, InjectedState]) -> str:
    """
    Herramienta útil para obtener la información del usuario que quiere registrar su inmueble.

    Usa esta herramienta para crear mensajes más personalizados para el usuario.
    """
    logger.info("Getting user info")
    chat_id = state.get("chat_id")
    chat_service = ChatService()
    user = chat_service.get_user_from_chat(chat_id)
    return user.name


@tool
def save_property_info(info: PropertyInfo, state: Annotated[dict, InjectedState]) -> Optional[Property]:
    """
    Herramienta útil para guardar la información de la propiedad en la base de datos.
    Checks for existing property first to prevent duplicates.
    """
    logger.info("Saving property info")
    chat_id = state.get("chat_id")
    property_service = PropertyService()
    chat_service = ChatService()
    
    # Get user from chat to use as owner
    user = chat_service.get_user_from_chat(chat_id)
    owner_id = user.id
    
    # Check if user already has a property
    existing_property_id = chat_service.get_property_id_from_chat(chat_id)
    
    if existing_property_id:
        # Update existing property with new info
        property_service.update_property(existing_property_id, info)
        
        # Ensure chat.property_id is set
        chat_service.update_chat(chat_id, {"property_id": existing_property_id})
        
        return property_service.get_property_full_info(existing_property_id)
    else:
        # Create new property
        property_obj = property_service.create_property(info, owner_id)
        
        # Set chat.property_id to link chat to property
        chat_service.update_chat(chat_id, {"property_id": property_obj.id})
        
        return property_obj


@tool
def get_remaining_info(state: Annotated[dict, InjectedState]) -> Optional[PropertyProgress]:
    """
    Herramienta útil para obtener la información que falta para completar el registro de la propiedad.
    """
    logger.info("Getting remaining info")
    # cast to str chat_id
    chat_id = state.get("chat_id") or ""
    
    # Try to get property_id from state first, then from chat service
    chat_service = ChatService()
    property_id = chat_service.get_property_id_from_chat(chat_id) 
    
    if not property_id:
        # Return progress indicating all PropertyInfo fields are missing
        return PropertyProgress(
            property_id="",
            current_stage="initial",
            missing_fields=["address", "type", "price"],
            completion_percentage=0.0
        )
    
    property_service = PropertyService()
    return property_service.get_progress_info(property_id)
