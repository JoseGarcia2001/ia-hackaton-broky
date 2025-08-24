"""
Defines the tools for the register agent.
"""

from typing import Optional
from langchain.tools import tool


from pydantic import BaseModel, Field


class UserInfo(BaseModel):
    name: str
    email: str


class PropertyInfo(BaseModel):
    """
    Información mínima para registrar una propiedad.
    """
    address: Optional[str] = Field(description="Dirección de la propiedad")
    type: Optional[str] = Field(description="Tipo de propiedad")
    price: Optional[str] = Field(description="Precio de la propiedad")



@tool
def get_user_info() -> UserInfo:
    """
    Herramienta útil para obtener la información del usuario que quiere registrar su inmueble.

    Usa esta herramienta para crear mensajes más personalizados para el usuario.
    """
    # TODO: Implement the tool to get the user info
    return UserInfo(name="Juan Perez", email="juan.perez@gmail.com").model_dump()


@tool
def save_property_info(info: PropertyInfo) -> str:
    """
    Herramienta útil para guardar la información de la propiedad en la base de datos.
    """
    # TODO: Implement the tool to save the property info
    return "Property info saved!"


@tool
def get_remaining_info() -> PropertyInfo:
    """
    Herramienta útil para obtener la información que falta para completar el registro de la propiedad.
    """
    # TODO: Implement the tool to get the remaining info
    return PropertyInfo(address="Calle 123 #45-67", type=None, price="350 millones de pesos").model_dump()


@tool
def generate_qr() -> str:
    """
    Herramienta útil para generar el código QR asociado a la propiedad.
    """
    # TODO: Implement the tool to generate the QR
    return "QR generated!"