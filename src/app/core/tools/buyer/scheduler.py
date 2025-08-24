"""
Defines the tools for the buyer scheduler agent
"""

from typing import Annotated
from langchain.tools import tool
from langgraph.prebuilt import InjectedState

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

    return "Notificación enviada correctamente"
