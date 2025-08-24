"""
OpenAI utils
"""
import os
import sys
import base64
import io
from typing import Optional

try:
    from PIL import Image
except ImportError:
    print("PIL not found. Install with: pip install Pillow")
    raise

try:
    from openai import OpenAI
except ImportError:
    print("OpenAI not found. Install with: pip install openai")
    raise

# Handle imports based on execution context
try:
    from ..config import settings
except ImportError:
    # For direct execution or testing
    sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
    try:
        from app.config import settings
    except ImportError:
        from src.app.config import settings


class OpenIA:
    def __init__(self):
        self.openai_client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
        )

    def extract_text_audio(self, audio_path: str) -> str:
        """Extract text from an audio file"""
        with open(audio_path, "rb") as f:
            try:
                transcription = self.openai_client.audio.transcriptions.create(
                    file=f,
                    model="whisper-1",
                )
                text = transcription.text
                print(f"Text extracted from audio: {text}")
                return text
            except Exception as e: # pylint: disable=broad-exception-caught
                print(f"Error extracting text from audio: {str(e)}")
                return ""

    def integrate_images_with_ai(
        self,
        phone_number: str,
        qr_message: Optional[str] = None
    ) -> str:
        """
        Integra un código QR con la imagen base usando OpenAI Images Edit API
        
        Args:
            phone_number (str): Número de teléfono para generar el QR
            qr_message (str, optional): Mensaje predefinido para el QR
            
        Returns:
            str: Ruta del archivo de imagen generado
        """
        try:
            # Importar WhatsAppQRGenerator localmente para evitar imports circulares
            try:
                from .whatsapp_qr import WhatsAppQRGenerator
            except ImportError:
                # Fallback for different execution contexts
                try:
                    from app.utils.whatsapp_qr import WhatsAppQRGenerator
                except ImportError:
                    from src.app.utils.whatsapp_qr import WhatsAppQRGenerator
            
            # 1. Generar QR de WhatsApp y guardarlo temporalmente
            qr_generator = WhatsAppQRGenerator()
            
            # Crear directorio temporal
            temp_dir = os.path.join(
                os.path.dirname(__file__), 
                "..", 
                "resources", 
                "temp"
            )
            os.makedirs(temp_dir, exist_ok=True)
            
            # Guardar QR temporal para OpenAI
            temp_qr_path = qr_generator.save_qr_image(
                phone_number=phone_number,
                message=qr_message,
                directory=temp_dir,
                filename="temp_qr.png",
                box_size=10,
                border=2
            )
            
            # 2. Cargar imagen base
            base_image_path = os.path.join(
                os.path.dirname(__file__), 
                "..", 
                "resources", 
                "qr", 
                "imagen_qr.png"
            )
            
            if not os.path.exists(base_image_path):
                raise FileNotFoundError(f"No se encontró la imagen base en: {base_image_path}")
            
            print(f"🖼️  Imagen base: {base_image_path}")
            print(f"📱 QR temporal: {temp_qr_path}")
            
            # 3. Preparar imagen para OpenAI (convertir a RGBA si es necesario)
            base_image = Image.open(base_image_path)
            
            # Convertir a RGBA si no está en ese formato
            if base_image.mode not in ['RGBA', 'LA', 'L']:
                print(f"🔄 Convirtiendo imagen de {base_image.mode} a RGBA para OpenAI...")
                base_image = base_image.convert('RGBA')
            
            # Guardar imagen temporal en formato RGBA
            temp_base_path = os.path.join(temp_dir, "temp_base_rgba.png")
            base_image.save(temp_base_path, "PNG")
            
            # 4. Usar OpenAI Images Edit API para integrar inteligentemente
            with open(temp_base_path, "rb") as base_file:
                response = self.openai_client.images.edit(
                    model="dall-e-2",
                    image=base_file,
                    prompt="Reemplaza el código QR que está en el centro del rectángulo blanco con este nuevo código QR de WhatsApp. Mantén exactamente el mismo diseño, colores y estilo de la imagen original. El nuevo QR debe estar perfectamente centrado en el rectángulo blanco y debe verse natural e integrado con el diseño. Conserva todos los elementos visuales: el texto 'SE VENDE', el fondo morado, y las casitas en la parte inferior. Adicional no me cambies el contenido del QR, solo el código QR. Y respeta las dimensiones de la imagen original",
                    n=1,
                    size="1024x1024",
                    response_format="b64_json"
                )
            
            # 5. Procesar respuesta de OpenAI
            if response.data and len(response.data) > 0:
                image_data = response.data[0]
                image_b64 = image_data.b64_json
                
                # 6. Guardar imagen resultado
                output_dir = os.path.join(
                    os.path.dirname(__file__), 
                    "..", 
                    "resources", 
                    "qr"
                )
                os.makedirs(output_dir, exist_ok=True)
                
                output_path = os.path.join(output_dir, "qr_completed.png")
                
                # Decodificar y guardar
                image_bytes = base64.b64decode(image_b64)
                with open(output_path, "wb") as f:
                    f.write(image_bytes)
                
                # 7. Limpiar archivos temporales
                try:
                    os.remove(temp_qr_path)
                    os.remove(temp_base_path)
                except Exception as cleanup_error:
                    print(f"⚠️  Advertencia limpiando archivos temporales: {cleanup_error}")
                
                print(f"✨ Imagen integrada con IA guardada en: {output_path}")
                return output_path
            else:
                raise Exception("OpenAI no retornó ninguna imagen")
            
        except Exception as e:
            print(f"❌ Error integrando con IA: {str(e)}")
            # Fallback al método manual
            print("🔄 Intentando método manual como respaldo...")
            return self.integrate_images_manual(phone_number, qr_message)
    
    def integrate_images(
        self, 
        phone_number: str, 
        qr_message: Optional[str] = None,
        replace_center_qr: bool = True,
        qr_position: Optional[tuple] = None,
        qr_size: Optional[tuple] = None
    ) -> str:
        """
        Método manual de integración (método de respaldo)
        
        Args:
            phone_number (str): Número de teléfono para generar el QR
            qr_message (str, optional): Mensaje predefinido para el QR
            replace_center_qr (bool): Si True, reemplaza automáticamente el QR central
            qr_position (tuple, optional): Posición (x, y) manual donde colocar el QR
            qr_size (tuple, optional): Tamaño (width, height) manual del QR
            
        Returns:
            str: Ruta del archivo de imagen generado
        """
        # Redirigir al método con IA por defecto
        if replace_center_qr and qr_position is None and qr_size is None:
            return self.integrate_images_with_ai(phone_number, qr_message)
        
        # Si no, usar método manual
        return self.integrate_images_manual(phone_number, qr_message, replace_center_qr, qr_position, qr_size)
    
    def integrate_images_manual(
        self, 
        phone_number: str, 
        qr_message: Optional[str] = None,
        replace_center_qr: bool = True,
        qr_position: Optional[tuple] = None,
        qr_size: Optional[tuple] = None
    ) -> str:
        """
        Integra un código QR de WhatsApp con la imagen base usando PIL (método manual)
        
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
            # Importar WhatsAppQRGenerator localmente para evitar imports circulares
            try:
                from .whatsapp_qr import WhatsAppQRGenerator
            except ImportError:
                # Fallback for different execution contexts
                try:
                    from app.utils.whatsapp_qr import WhatsAppQRGenerator
                except ImportError:
                    from src.app.utils.whatsapp_qr import WhatsAppQRGenerator
            
            # 1. Generar QR de WhatsApp en base64
            qr_generator = WhatsAppQRGenerator()
            qr_base64 = qr_generator.get_qr_base64(
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
                # Calcular automáticamente la posición y tamaño del QR central
                qr_position, qr_size = self._calculate_center_qr_area(base_image)
                print(f"QR central detectado - Posición: {qr_position}, Tamaño: {qr_size}")
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
            
            # 7. Reemplazar/superponer QR en la imagen base
            if replace_center_qr:
                # Limpiar el área del QR central antes de colocar el nuevo
                self._clear_qr_area(base_image, qr_position, qr_size)
            
            # Optimizar el QR para mejor integración
            qr_image = self._optimize_qr_for_integration(qr_image)
            
            # Colocar el nuevo QR
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
            print(f"Error integrando imágenes: {str(e)}")
            raise
    
    def _calculate_center_qr_area(self, base_image: Image.Image) -> tuple:
        """
        Calcula automáticamente la posición y tamaño del área del QR central
        
        Args:
            base_image: Imagen base PIL
            
        Returns:
            tuple: ((x, y), (width, height)) - posición y tamaño del QR central
        """
        img_width, img_height = base_image.size
        
        # Basado en la imagen mostrada, el QR está en el rectángulo blanco central
        # El rectángulo blanco ocupa aproximadamente 65% del ancho y está centrado
        
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
    
    def _clear_qr_area(self, base_image: Image.Image, position: tuple, size: tuple):
        """
        Limpia el área del QR central rellenándola con el color de fondo
        
        Args:
            base_image: Imagen base PIL
            position: Posición (x, y) del área a limpiar
            size: Tamaño (width, height) del área a limpiar
        """
        try:
            from PIL import ImageDraw
        except ImportError:
            print("PIL ImageDraw not available, skipping area clearing")
            return
        
        # Crear un objeto para dibujar
        draw = ImageDraw.Draw(base_image)
        
        # Para el fondo del área del QR, usamos blanco (color del rectángulo)
        # Ya que el QR original está sobre un fondo blanco
        background_color = (255, 255, 255, 255)  # Blanco sólido RGBA
        
        # Limpiar el área rectangular con un margen extra para cubrir completamente
        x, y = position
        width, height = size
        
        # Añadir un pequeño margen para asegurar cobertura completa
        margin = 5
        draw.rectangle([
            x - margin, 
            y - margin, 
            x + width + margin, 
            y + height + margin
        ], fill=background_color)
        
        print(f"🧹 Área limpiada: ({x-margin}, {y-margin}) a ({x+width+margin}, {y+height+margin})")
    
    def _get_background_color(self, base_image: Image.Image, position: tuple, size: tuple) -> tuple:
        """
        Obtiene el color de fondo dominante alrededor del área del QR
        
        Args:
            base_image: Imagen base PIL
            position: Posición del QR
            size: Tamaño del QR
            
        Returns:
            tuple: Color RGBA del fondo
        """
        # Analizar píxeles alrededor del área del QR para obtener el color de fondo
        x, y = position
        width, height = size
        
        # Tomar muestras de píxeles del borde del área del QR
        sample_points = [
            (x - 10, y + height // 2),  # Izquierda
            (x + width + 10, y + height // 2),  # Derecha  
            (x + width // 2, y - 10),  # Arriba
            (x + width // 2, y + height + 10)  # Abajo
        ]
        
        colors = []
        for px, py in sample_points:
            if 0 <= px < base_image.width and 0 <= py < base_image.height:
                pixel = base_image.getpixel((px, py))
                if isinstance(pixel, int):  # Escala de grises
                    pixel = (pixel, pixel, pixel, 255)
                elif len(pixel) == 3:  # RGB
                    pixel = pixel + (255,)  # Agregar alpha
                colors.append(pixel)
        
        if colors:
            # Promedio de los colores muestreados
            avg_color = tuple(sum(c[i] for c in colors) // len(colors) for i in range(4))
            return avg_color
        else:
            # Color de fondo por defecto (blanco semi-transparente)
            return (255, 255, 255, 200)
    
    def _optimize_qr_for_integration(self, qr_image: Image.Image) -> Image.Image:
        """
        Optimiza el QR para mejor integración visual
        
        Args:
            qr_image: Imagen QR original
            
        Returns:
            Image.Image: QR optimizado
        """
        # Asegurar que el QR tenga alta calidad y bordes limpios
        if qr_image.mode != 'RGBA':
            qr_image = qr_image.convert('RGBA')
        
        # Aplicar un pequeño filtro para mejorar la nitidez
        try:
            from PIL import ImageFilter
            # Aplicar un ligero sharpen para bordes más definidos
            qr_image = qr_image.filter(ImageFilter.SHARPEN)
        except ImportError:
            pass  # Si no está disponible ImageFilter, continuar sin filtro
        
        return qr_image
