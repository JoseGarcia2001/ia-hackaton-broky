"""
Defines the tools for the register agent.
"""

from langchain.tools import tool


# TODO: Use pydantic models for seller info
@tool
def get_user_info() -> dict:
    """
    Herramienta útil para obtener la información del usuario que quiere registrar su inmueble.

    Usa esta herramienta para crear mensajes más personalizados para el usuario.
    """
    return {"name": "Juan Perez", "email": "juan.perez@gmail.com"}


# TODO: Use pydantic models for property info
@tool
def save_property_info(info: dict) -> str:
    """
    Herramienta útil para guardar la información de la propiedad en la base de datos.
    """
    return "Property info saved!"


@tool
def get_remaining_info() -> dict:
    """
    Herramienta útil para obtener la información que falta para completar el registro de la propiedad.
    """
    return {"address": "Calle 123 #45-67", "type": None, "price": "350 millones de pesos"}
