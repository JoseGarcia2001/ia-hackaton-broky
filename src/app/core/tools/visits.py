"""
Defines the tools for the visits agent
- Create a property card with all the information relevant to the visit.
"""

from typing import Annotated, Optional
from langchain.tools import tool
from langgraph.prebuilt import InjectedState


@tool
def create_property_card(state: Annotated[dict, InjectedState]) -> str:
    """
    Herramienta útil para crear una ficha detallada de la propiedad.
    """
    # TODO: Implement the logic
    return "Ficha de la propiedad creada correctamente"


@tool
def get_appraisal_info(state: Annotated[dict, InjectedState]) -> str:
    """
    Herramienta útil para obtener la información de avalúo de la propiedad.
    """
    # TODO: Implement the logic
    return "Información de avalúo obtenida correctamente"


@tool
def publish_property(state: Annotated[dict, InjectedState]) -> str:
    """
    Herramienta útil para publicar la propiedad en las plataformas digitales.
    """
    # TODO: Implement the logic
    return "Propiedad publicada correctamente"