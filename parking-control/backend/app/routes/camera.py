from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.auth import get_current_user
from app.utils.camera import process_vehicle_image, upload_image_to_s3
from app.models.models import Vehicle as VehicleModel
import cv2
import numpy as np
from datetime import datetime

router = APIRouter()

@router.post("/process-entry")
async def process_vehicle_entry(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        # Ler imagem do upload
        contents = await file.read()
        nparr = np.fromstring(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Processar imagem para detectar placa
        plate_number = process_vehicle_image(image)
        
        if not plate_number:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Não foi possível detectar a placa do veículo"
            )
        
        # Buscar veículo pela placa
        vehicle = db.query(VehicleModel).filter(
            VehicleModel.plate == plate_number
        ).first()
        
        if not vehicle:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Veículo com placa {plate_number} não encontrado"
            )
        
        # Upload da imagem para S3
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_key = f"entries/{plate_number}_{timestamp}.jpg"
        image_url = upload_image_to_s3(contents, image_key)
        
        return {
            "plate_number": plate_number,
            "vehicle_id": vehicle.id,
            "image_url": image_url,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/process-exit")
async def process_vehicle_exit(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        # Similar ao process_vehicle_entry, mas para saída
        contents = await file.read()
        nparr = np.fromstring(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        plate_number = process_vehicle_image(image)
        
        if not plate_number:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Não foi possível detectar a placa do veículo"
            )
        
        # Upload da imagem para S3
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_key = f"exits/{plate_number}_{timestamp}.jpg"
        image_url = upload_image_to_s3(contents, image_key)
        
        return {
            "plate_number": plate_number,
            "image_url": image_url,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        ) 