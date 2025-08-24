"""
Servicio para integración de imágenes QR de WhatsApp
"""

from typing import Optional
from ..utils.whatsapp_qr import WhatsAppQRGenerator
from PIL import Image
import os
import base64
import io


class ImageIntegrationService:
    """Servicio para integrar códigos QR de WhatsApp con imágenes base"""

    def __init__(self):
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
                "¡Hola! 🏠 Me gustaría obtener información sobre esta propiedad."
            )

        return self._integrate_qr_image(
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

        return self._integrate_qr_image(
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

            # Prueba 2: Integración de imagen manual
            print("✨ Integrando QR con imagen base usando método manual...")
            result_path = self.create_property_qr_image(
                phone_number=test_phone,
                property_message="🏠 ¡Propiedad de prueba disponible! Contacta para más información.",
                replace_center_qr=True,  # Usa método manual centrado
            )

            print(f"✅ Imagen integrada creada en: {result_path}")

            # Prueba 3: Verificar archivo generado

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
    
    def _integrate_qr_image(
        self, 
        phone_number: str, 
        qr_message: Optional[str] = None,
        replace_center_qr: bool = True,
        qr_position: Optional[tuple] = None,
        qr_size: Optional[tuple] = None
    ) -> str:
        """
        Integra un código QR de WhatsApp con la imagen base usando PIL (sin OpenAI)
        
        Args:
            phone_number (str): Número de teléfono para generar el QR
            qr_message (str, optional): Mensaje predefinido para el QR
            replace_center_qr (bool): Si True, reemplaza automáticamente el QR central
            qr_position (tuple, optional): Posición (x, y) manual donde colocar el QR
            qr_size (tuple, optional): Tamaño (width, height) manual del QR
            
        Returns:
            str: Ruta del archivo de imagen generado
        """
        try:
            # 1. Generar QR de WhatsApp en base64
            qr_base64 = self.qr_generator.get_qr_base64(
                phone_number=phone_number,
                message=qr_message,
                fill_color="black",
                back_color="white",
                box_size=8,  # QR más nítido
                border=2     # Borde más pequeño para mejor ajuste
            )
            
            # 2. Convertir QR base64 a imagen PIL
            qr_image_data = base64.b64decode(qr_base64)
            qr_image = Image.open(io.BytesIO(qr_image_data))
            
            # 3. Cargar imagen base
            base_image_path = os.path.join(
                os.path.dirname(__file__), 
                "..", 
                "resources", 
                "qr", 
                "imagen_qr.png"
            )
            
            if not os.path.exists(base_image_path):
                raise FileNotFoundError(f"No se encontró la imagen base en: {base_image_path}")
            
            base_image = Image.open(base_image_path)
            
            # 4. Determinar posición y tamaño del QR
            if replace_center_qr:
                # Usar las dimensiones de las líneas 337-339 de openai.py
                qr_position, qr_size = self._calculate_center_qr_area(base_image)
                print(f"QR central calculado - Posición: {qr_position}, Tamaño: {qr_size}")
            else:
                # Usar valores por defecto si no se especifican
                if qr_position is None:
                    qr_position = (50, 50)
                if qr_size is None:
                    qr_size = (200, 200)
            
            # 5. Redimensionar QR al tamaño calculado/especificado
            qr_image = qr_image.resize(qr_size, Image.Resampling.LANCZOS)
            
            # 6. Convertir imágenes a RGBA para manejar transparencia
            if base_image.mode != 'RGBA':
                base_image = base_image.convert('RGBA')
            if qr_image.mode != 'RGBA':
                qr_image = qr_image.convert('RGBA')
            
            # 7. Colocar el nuevo QR en la imagen base
            base_image.paste(qr_image, qr_position, qr_image)
            
            # 8. Crear directorio de salida si no existe
            output_dir = os.path.join(
                os.path.dirname(__file__), 
                "..", 
                "resources", 
                "qr"
            )
            os.makedirs(output_dir, exist_ok=True)
            
            # 9. Guardar imagen resultado
            output_path = os.path.join(output_dir, "qr_completed.png")
            base_image.save(output_path, "PNG")
            
            print(f"Imagen integrada guardada en: {output_path}")
            return output_path
            
        except Exception as e:
            error_message = f"❌ Error integrando imagen QR: {str(e)}"
            print(error_message)
            raise e
    
    def _calculate_center_qr_area(self, base_image: Image.Image) -> tuple:
        """
        Calcula la posición y tamaño óptimos para el QR central
        Basado en las dimensiones de las líneas 337-339 de openai.py
        
        Args:
            base_image: Imagen base PIL
            
        Returns:
            tuple: ((x, y), (width, height)) - posición y tamaño del QR
        """
        img_width, img_height = base_image.size
        
        # Basado en las líneas 337-339 de openai.py:
        # Calcular el área del rectángulo blanco central
        white_rect_width = int(img_width * 0.65)  # 65% del ancho total
        white_rect_height = int(img_height * 0.45)  # Aproximadamente 45% del alto
        
        # El QR dentro del rectángulo blanco ocupa aproximadamente 90% del rectángulo
        qr_width = int(white_rect_width * 0.90)
        qr_height = int(white_rect_height * 0.85)  # Ligeramente menos alto para mejor ajuste
        
        # Centrar perfectamente en la imagen
        center_x = img_width // 2
        center_y = int(img_height * 0.46)  # El rectángulo blanco está ligeramente arriba del centro
        
        # Calcular posición de la esquina superior izquierda del QR
        qr_x = center_x - (qr_width // 2)
        qr_y = center_y - (qr_height // 2)
        
        print(f"📐 Imagen: {img_width}x{img_height}, QR calculado: {qr_width}x{qr_height} en posición ({qr_x}, {qr_y})")
        
        return (qr_x, qr_y), (qr_width, qr_height)
