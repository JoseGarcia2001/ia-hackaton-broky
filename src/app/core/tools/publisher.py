"""
Defines tools for publisher agent
"""
from typing import Annotated, Optional

from langchain.tools import tool
from langgraph.prebuilt import InjectedState


from ...config import settings
from ...services.image_integration_service import ImageIntegrationService
from ...services.property_service import PropertyService
from ...services.chat_service import ChatService
from ...services.qr_service import QRResponse
from ...utils.logger import logger
from ...utils.s3_utils import upload_file_to_s3
from ...services.infobip_service import InfobipService



@tool
def generate_qr(state: Annotated[dict, InjectedState]) -> Optional[QRResponse]:
    """
    Herramienta útil para generar el código QR asociado a la propiedad.
    """
    logger.info("Generating QR")
    chat_id = state.get("chat_id")
    chat_service = ChatService()
    user_data = chat_service.get_user_from_chat(chat_id)
    property_id = chat_service.get_property_id_from_chat(chat_id)
    phone_number = user_data.phone
    property_service = PropertyService()
    property_obj = property_service.get_property_full_info(property_id)
    address = property_obj.address
    integration_service = ImageIntegrationService()
    qr_position = None
    qr_size = None
    path = integration_service.create_property_qr_image(
        phone_number=settings.INFOBIP_WHATSAPP_FROM,
        property_message=f"¡Hola! 🏠 Me gustaría obtener información sobre la propiedad ubicada en {address}",
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