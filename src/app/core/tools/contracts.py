"""
Defines the tools for contract management after completed deals
- Generate sales contract (contrato de compra y venta)
- Manage legal documentation
- Handle contract finalization
"""

import os
import random
from typing import Annotated
from datetime import datetime, timedelta
from langchain.tools import tool
from langgraph.prebuilt import InjectedState

from src.app.utils.logger import logger
from src.app.utils.s3_utils import upload_file_to_s3
from src.app.services.chat_service import ChatService
from src.app.services.infobip_service import InfobipService


@tool
def generate_sales_contract(buyer_info: str, state: Annotated[dict, InjectedState]) -> str:
    """
    Herramienta útil para generar el contrato de compra y venta entre el comprador y vendedor.
    Sube el PDF del contrato a S3 y lo envía por InfobipService (siguiendo la misma lógica que el QR).
    
    Args:
        buyer_info: Información básica del comprador (nombre, identificación, etc.)
    """
    logger.info("Generating sales contract PDF")
    
    try:
        chat_id = state.get("chat_id")
        chat_service = ChatService()
        user_data = chat_service.get_user_from_chat(chat_id)
        phone_number = user_data.phone
        
        # Get local PDF contract path (same pattern as QR tool)
        contract_pdf_path = os.path.join(
            os.path.dirname(__file__), 
            "..", "..", 
            "resources", 
            "contracts", 
            "FORMATO-CONTRATO-DE-COMPRAVENTA.pdf"
        )
        
        # Upload contract PDF to S3 (following exact same pattern as QR tool)
        url_public = upload_file_to_s3(contract_pdf_path)
        
        if url_public:
            
            return {
                "success": True,
                # simple message w url
                "message": f"Contrato de Compra y Venta Generado\nDocumento del Contrato (PDF):\n🔗 {url_public}"

            }

        else:
            logger.error("Failed to upload contract PDF to S3")
            return {
                "success": False,
                "message": "❌ **Error al generar contrato**\n\nNo se pudo generar el enlace del contrato PDF."
            }
            
    except Exception as e:
        logger.error(f"Error generating sales contract: {str(e)}")
        return {
            "success": False,
            "message": f"❌ **Error al generar contrato**\n\nOcurrió un error: {str(e)}"
        }

