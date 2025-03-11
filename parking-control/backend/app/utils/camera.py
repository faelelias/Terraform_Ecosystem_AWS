import cv2
import numpy as np
import boto3
from app.config import settings
import io
from PIL import Image

def process_vehicle_image(image: np.ndarray) -> str:
    """
    Processa a imagem do veículo para detectar a placa.
    Esta é uma implementação básica que deve ser substituída por um
    sistema mais robusto de OCR/ALPR como o OpenALPR ou AWS Rekognition.
    """
    # TODO: Implementar reconhecimento de placa real
    # Por enquanto, retorna None para indicar que precisa ser implementado
    return None

def upload_image_to_s3(image_bytes: bytes, key: str) -> str:
    """
    Faz upload da imagem para o S3 e retorna a URL.
    """
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region
        )
        
        # Converter para formato JPEG e otimizar
        image = Image.open(io.BytesIO(image_bytes))
        output = io.BytesIO()
        image.save(output, format='JPEG', optimize=True, quality=85)
        output.seek(0)
        
        # Upload para S3
        s3_client.upload_fileobj(
            output,
            settings.s3_bucket,
            key,
            ExtraArgs={'ContentType': 'image/jpeg'}
        )
        
        # Gerar URL
        url = f"https://{settings.s3_bucket}.s3.{settings.aws_region}.amazonaws.com/{key}"
        return url
        
    except Exception as e:
        print(f"Erro ao fazer upload para S3: {str(e)}")
        raise 