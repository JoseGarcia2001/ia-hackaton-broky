"""
Utilitario para generar códigos QR que enlazan a WhatsApp con mensajes predefinidos.

Este módulo proporciona funcionalidades para:
- Generar URLs de WhatsApp con mensajes predeterminados
- Crear códigos QR que redirigen a WhatsApp
- Guardar códigos QR como imágenes
"""

import os
import io
import qrcode
import base64
from PIL import Image
from typing import Optional
from urllib.parse import quote


class WhatsAppQRGenerator:
    """Generador de códigos QR para WhatsApp."""
    
    def __init__(self):
        self.base_url = "https://wa.me/"
    
    def generate_whatsapp_url(
        self, 
        phone_number: str, 
        message: Optional[str] = None
    ) -> str:
        """
        Genera una URL de WhatsApp con un mensaje predefinido.
        
        Args:
            phone_number (str): Número de teléfono con código de país (ej: 57310xxxxxxx)
            message (str, optional): Mensaje predefinido
            
        Returns:
            str: URL de WhatsApp
        """
        # Limpiar número de teléfono (remover espacios, guiones, etc.)
        clean_phone = ''.join(filter(str.isdigit, phone_number))
        
        # Construir URL base
        url = f"{self.base_url}{clean_phone}"
        
        # Agregar mensaje si se proporciona
        if message:
            encoded_message = quote(message)
            url += f"?text={encoded_message}"
        
        return url
    
    def generate_qr_code(
        self,
        phone_number: str,
        message: Optional[str] = None,
        box_size: int = 10,
        border: int = 4
    ) -> qrcode.QRCode:
        """
        Genera un código QR para WhatsApp.
        
        Args:
            phone_number (str): Número de teléfono con código de país
            message (str, optional): Mensaje predefinido
            box_size (int): Tamaño de cada caja del QR (default: 10)
            border (int): Grosor del borde (default: 4)
            
        Returns:
            qrcode.QRCode: Objeto QR Code
        """
        # Generar URL de WhatsApp
        whatsapp_url = self.generate_whatsapp_url(phone_number, message)
        
        # Crear código QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=box_size,
            border=border,
        )
        
        qr.add_data(whatsapp_url)
        qr.make(fit=True)
        
        return qr
    
    def create_qr_image(
        self,
        phone_number: str,
        message: Optional[str] = None,
        fill_color: str = "black",
        back_color: str = "white",
        box_size: int = 10,
        border: int = 4
    ) -> Image.Image:
        """
        Crea una imagen del código QR.
        
        Args:
            phone_number (str): Número de teléfono con código de país
            message (str, optional): Mensaje predefinido
            fill_color (str): Color del QR
            back_color (str): Color de fondo
            box_size (int): Tamaño de cada caja del QR
            border (int): Grosor del borde
            
        Returns:
            PIL.Image.Image: Imagen del código QR
        """
        qr = self.generate_qr_code(
            phone_number, message, box_size, border
        )
        
        return qr.make_image(fill_color=fill_color, back_color=back_color)
    
    def save_qr_image(
        self,
        phone_number: str,
        message: Optional[str] = None,
        filename: Optional[str] = None,
        directory: str = "qr_codes",
        format: str = "PNG",
        **qr_params
    ) -> str:
        """
        Guarda el código QR como archivo de imagen.
        
        Args:
            phone_number (str): Número de teléfono con código de país
            message (str, optional): Mensaje predefinido
            filename (str, optional): Nombre del archivo (auto-generado si no se especifica)
            directory (str): Directorio donde guardar la imagen
            format (str): Formato de imagen (PNG, JPEG, etc.)
            **qr_params: Parámetros adicionales para el QR
            
        Returns:
            str: Ruta del archivo guardado
        """
        # Crear directorio si no existe
        os.makedirs(directory, exist_ok=True)
        
        # Generar nombre de archivo si no se proporciona
        if not filename:
            clean_phone = ''.join(filter(str.isdigit, phone_number))
            filename = f"whatsapp_qr_{clean_phone}.png"
        
        # Asegurar extensión correcta
        if not filename.lower().endswith(f'.{format.lower()}'):
            filename += f'.{format.lower()}'
        
        # Crear imagen QR
        qr_image = self.create_qr_image(phone_number, message, **qr_params)
        
        # Guardar imagen
        filepath = os.path.join(directory, filename)
        qr_image.save(filepath, format=format)
        
        return filepath
    
    def get_qr_base64(
        self,
        phone_number: str,
        message: Optional[str] = None,
        format: str = "PNG",
        **qr_params
    ) -> str:
        """
        Obtiene el código QR como string base64.
        
        Args:
            phone_number (str): Número de teléfono con código de país
            message (str, optional): Mensaje predefinido
            format (str): Formato de imagen
            **qr_params: Parámetros adicionales para el QR
            
        Returns:
            str: Imagen codificada en base64
        """
        # Crear imagen QR
        qr_image = self.create_qr_image(phone_number, message, **qr_params)
        
        # Convertir a base64
        buffered = io.BytesIO()
        qr_image.save(buffered, format=format)
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return img_str
