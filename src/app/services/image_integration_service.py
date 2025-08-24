"""
Servicio para integración de imágenes QR de WhatsApp
"""

from typing import Optional
from ..utils.openai import OpenIA
from ..utils.whatsapp_qr import WhatsAppQRGenerator


class ImageIntegrationService:
    """Servicio para integrar códigos QR de WhatsApp con imágenes base"""

    def __init__(self):
        self.openai_service = OpenIA()
        self.qr_generator = WhatsAppQRGenerator()

    def create_property_qr_image(
        self,
        phone_number: str,
        property_message: Optional[str] = None,
        replace_center_qr: bool = True,
        qr_position: Optional[tuple] = None,
        qr_size: Optional[tuple] = None,
    ) -> str:
        """
        Crea una imagen integrada con QR de WhatsApp para una propiedad

        Args:
            phone_number (str): Número de teléfono del contacto
            property_message (str, optional): Mensaje personalizado para la propiedad
            replace_center_qr (bool): Si True, reemplaza automáticamente el QR central
            qr_position (tuple, optional): Posición manual donde colocar el QR
            qr_size (tuple, optional): Tamaño manual del QR

        Returns:
            str: Ruta de la imagen generada
        """
        if not property_message:
            property_message = (
                "¡Hola Broky! 🏠 Me gustaría obtener información sobre esta propiedad."
            )

        return self.openai_service.integrate_images(
            phone_number=phone_number,
            qr_message=property_message,
            replace_center_qr=replace_center_qr,
            qr_position=qr_position,
            qr_size=qr_size,
        )

    def create_contact_qr_image(
        self,
        phone_number: str,
        contact_name: Optional[str] = None,
        replace_center_qr: bool = True,
        qr_position: Optional[tuple] = None,
        qr_size: Optional[tuple] = None,
    ) -> str:
        """
        Crea una imagen integrada con QR de WhatsApp para contacto general

        Args:
            phone_number (str): Número de teléfono del contacto
            contact_name (str, optional): Nombre del contacto
            replace_center_qr (bool): Si True, reemplaza automáticamente el QR central
            qr_position (tuple, optional): Posición manual donde colocar el QR
            qr_size (tuple, optional): Tamaño manual del QR

        Returns:
            str: Ruta de la imagen generada
        """
        if contact_name:
            message = f"¡Hola {contact_name}! 👋 Me gustaría ponerme en contacto contigo a través de Broky."
        else:
            message = (
                "¡Hola! 👋 Me gustaría ponerme en contacto contigo a través de Broky."
            )

        return self.openai_service.integrate_images(
            phone_number=phone_number,
            qr_message=message,
            replace_center_qr=replace_center_qr,
            qr_position=qr_position,
            qr_size=qr_size,
        )

    def test_integration(self, test_phone: str = "573001234567") -> dict:
        """
        Método de prueba para verificar la funcionalidad de integración

        Args:
            test_phone (str): Número de teléfono de prueba

        Returns:
            dict: Resultado de la prueba con información detallada
        """
        try:
            print("🧪 Iniciando prueba de integración de imágenes...")

            # Prueba 1: QR básico de WhatsApp
            print("📱 Generando QR básico de WhatsApp...")
            qr_base64 = self.qr_generator.get_qr_base64(
                phone_number=test_phone, message="Hola! Esta es una prueba de Broky 🏠"
            )
            print(f"✅ QR base64 generado (longitud: {len(qr_base64)} caracteres)")

            # Prueba 2: Integración de imagen con IA
            print("✨ Integrando QR con imagen base usando OpenAI IA...")
            result_path = self.create_property_qr_image(
                phone_number=test_phone,
                property_message="🏠 ¡Propiedad de prueba disponible! Contacta para más información.",
                replace_center_qr=True,  # Esto usa OpenAI IA automáticamente
            )

            print(f"✅ Imagen integrada creada en: {result_path}")

            # Prueba 3: Verificar archivo generado
            import os

            if os.path.exists(result_path):
                file_size = os.path.getsize(result_path)
                print(f"📊 Tamaño del archivo: {file_size} bytes")
            else:
                raise FileNotFoundError("El archivo no se generó correctamente")

            return {
                "success": True,
                "message": "Prueba de integración completada exitosamente",
                "qr_base64_length": len(qr_base64),
                "result_path": result_path,
                "file_size": file_size,
                "test_phone": test_phone,
            }

        except Exception as e:
            error_message = f"❌ Error en prueba de integración: {str(e)}"
            print(error_message)
            return {"success": False, "message": error_message, "error": str(e)}
