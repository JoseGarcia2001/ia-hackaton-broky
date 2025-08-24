import boto3
import uuid
import os
from typing import Optional
from botocore.exceptions import NoCredentialsError, ClientError
from src.app.config import settings


def upload_file_to_s3(file_path: str, bucket_name: str = "broky-images", folder: str = "uploads") -> Optional[str]:
    """
    Sube un archivo a S3 con un nombre aleatorio y devuelve la URL pública.
    
    Args:
        file_path (str): Ruta del archivo local a subir
        bucket_name (str): Nombre del bucket de S3
        folder (str): Carpeta dentro del bucket (por defecto "uploads")
    
    Returns:
        str: URL pública del archivo subido, None si hay error
    """
    try:
        # Verificar que el archivo existe
        if not os.path.exists(file_path):
            print(f"Error: El archivo {file_path} no existe")
            return None
        
        # Crear cliente S3
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_SECRET_KEY,
            region_name=settings.AWS_REGION
        )
        file_extension = os.path.splitext(file_path)[1]
        
        # Generar nombre aleatorio para el archivo
        random_filename = f"{uuid.uuid4().hex}{file_extension}"
        
        # Crear la key completa (ruta en S3)
        s3_key = f"{folder}/{random_filename}"
        
        # Subir el archivo
        s3_client.upload_file(
            file_path,
            bucket_name,
            s3_key,
        )
        
        # Construir la URL pública
        public_url = f"https://{bucket_name}.s3.{settings.AWS_REGION}.amazonaws.com/{s3_key}"
        
        print(f"Archivo subido exitosamente: {public_url}")
        return public_url
        
    except NoCredentialsError:
        print("Error: Credenciales de AWS no encontradas")
        return None
    except ClientError as e:
        print(f"Error del cliente S3: {e}")
        return None
    except FileNotFoundError as e:
        print(f"Error: Archivo no encontrado: {e}")
        return None
    except Exception as e:
        print(f"Error inesperado: {e}")
        return None
