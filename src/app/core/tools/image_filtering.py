from langchain_core.tools import tool
from typing import Annotated
from app.services.infobip_service import InfobipService
from app.utils.openai import OpenIA


@tool
def filter_image(
    url: Annotated[str, "La url de la imagen a procesar"],
) -> str:
    """Filtra una imagen"""
    path = InfobipService().save_file(url)
    path_with_filter = OpenIA().prettify_image(path)
    return path_with_filter
