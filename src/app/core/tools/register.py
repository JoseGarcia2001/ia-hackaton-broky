"""
Defines the tools for the register agent.
"""

from typing import Annotated, Optional, Dict, Any
from langchain.tools import tool
from pydantic import BaseModel, Field
from langgraph.prebuilt import InjectedState
from ...services.image_integration_service import ImageIntegrationService
from ...utils.s3_utils import upload_file_to_s3

from ...services.property_service import PropertyService, PropertyInfo, PropertyProgress
from ...services.chat_service import ChatService
from ...models.property import Property
from ...models.user import User
from ...services.infobip_service import InfobipService


class UserInfo(BaseModel):
    name: str
    email: str


class PropertyInfo(BaseModel):
    """
    Información mínima para registrar una propiedad.
    """

    address: Optional[str] = Field(description="Dirección de la propiedad")
    type: Optional[str] = Field(description="Tipo de propiedad")
    price: Optional[float] = Field(description="Precio de la propiedad")


@tool
def get_user_info() -> UserInfo:
    """
    Herramienta útil para obtener la información del usuario que quiere registrar su inmueble.

    Usa esta herramienta para crear mensajes más personalizados para el usuario.
    """
    # TODO: Implement the tool to get the user info
    return UserInfo(name="Juan Perez", email="juan.perez@gmail.com").model_dump()


@tool
def save_property_info(info: PropertyInfo, state: Annotated[dict, InjectedState]) -> Optional[Property]:
    """
    Herramienta útil para guardar la información de la propiedad en la base de datos.
    """
    chat_id = state.get("chat_id")
    property_service = PropertyService()
    chat_service = ChatService()
    
    # Get user from chat to use as owner
    user = chat_service.get_user_from_chat(chat_id)
    owner_id = user.id
    
    property_obj = property_service.create_property(info, owner_id)
    
    return property_obj


@tool
def get_remaining_info(state: Annotated[dict, InjectedState]) -> Optional[PropertyProgress]:
    """
    Herramienta útil para obtener la información que falta para completar el registro de la propiedad.
    """
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
    


@tool
def generate_qr(phone_number: str, property_id: str) -> str:
    """
    Herramienta útil para generar el código QR asociado a la propiedad.
    """
    integration_service = ImageIntegrationService()
    qr_position = None
    qr_size = None
    path = integration_service.create_property_qr_image(
        phone_number=phone_number,
        property_message=f"¡Hola! 🏠 Me gustaría obtener información sobre la propiedad ubicada en {property_id}",
        replace_center_qr=True,
        qr_position=qr_position,
        qr_size=qr_size,
    )
    url_public = upload_file_to_s3(path)
    InfobipService().send_template_message(
        to=phone_number,
        template_name="banner_qr_broky",
        language="es",
        template_data={
            "image": url_public
        }
    )
    return {
        "success": True,
        "message": "Código QR generado y enviado correctamente",
    }
