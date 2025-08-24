"""
Defines the tools for the register agent.
"""

from typing import Annotated, Optional, Dict, Any
from langchain.tools import tool
from pydantic import BaseModel, Field
from langgraph.prebuilt import InjectedState

from ...services.property_service import PropertyService, PropertyInfo, PropertyProgress
from ...services.chat_service import ChatService, get_property_id_from_chat
from ...models.property import Property
from ...models.user import User


class UserInfo(BaseModel):
    name: str
    email: str





@tool
def get_user_info() -> UserInfo:
    """
    Herramienta útil para obtener la información del usuario que quiere registrar su inmueble.

    Usa esta herramienta para crear mensajes más personalizados para el usuario.
    """
    # TODO: Implement the tool to get the user info
    return UserInfo(name="Juan Perez", email="juan.perez@gmail.com").model_dump()


@tool
async def save_property_info(info: PropertyInfo, state: Annotated[dict, InjectedState]) -> Optional[Property]:
    """
    Herramienta útil para guardar la información de la propiedad en la base de datos.
    """
    chat_id = state.get("chat_id")
    property_service = PropertyService()
    chat_service = ChatService()
    
    # Get user from chat to use as owner
    user = await chat_service.get_user_from_chat(chat_id)
    owner_id = user.id
    
    property_obj = await property_service.create_property(info, owner_id)
    
    return property_obj


@tool
async def get_remaining_info(state: Annotated[dict, InjectedState]) -> Optional[PropertyProgress]:
    """
    Herramienta útil para obtener la información que falta para completar el registro de la propiedad.
    """
    # cast to str chat_id
    chat_id = state.get("chat_id") or ""
    
    # Try to get property_id from state first, then from chat service
    
    property_id = get_property_id_from_chat(chat_id) 
    
    if not property_id:
        return None
    
    property_service = PropertyService()
    return await property_service.get_progress_info(property_id)
    


@tool
def generate_qr() -> str:
    """
    Herramienta útil para generar el código QR asociado a la propiedad.
    """
    # TODO: Implement the tool to generate the QR
    return "QR generated!"
