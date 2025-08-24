"""
Defines the tools for the visits agent
- Create a property card with all the information relevant to the visit.
"""

import random
from typing import Annotated
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
def get_appraisal_info(_: Annotated[dict, InjectedState]) -> str:
    """
    Herramienta útil para obtener la información de avalúo de la propiedad.
    """
    value = random.randint(30, 50) * 10000000
    value_str = "{:,.0f}".format(value)
    value_str = value_str.replace(",", ".")
    return f"Después de analizar tu propiedad, te informo que el avalúo aproximado es de ${value_str} de pesos colombianos"


@tool
def publish_property(state: Annotated[dict, InjectedState]) -> str:
    """
    Herramienta útil para publicar la propiedad en las plataformas digitales.
    """
    # TODO: Implement the logic
    return "Propiedad publicada correctamente"