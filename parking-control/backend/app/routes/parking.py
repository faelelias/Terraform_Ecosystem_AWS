from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.schemas import (
    ParkingSpotCreate,
    ParkingSpot,
    ParkingSpotWithVehicle,
    ParkingMapResponse,
    ParkingRecordCreate,
    ParkingRecord
)
from app.models.models import (
    ParkingSpot as ParkingSpotModel,
    ParkingRecord as ParkingRecordModel,
    Vehicle as VehicleModel
)
from app.utils.auth import get_current_user
from datetime import datetime

router = APIRouter()

@router.get("/map", response_model=List[ParkingMapResponse])
def get_parking_map(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Agrupar vagas por andar
    floors = db.query(ParkingSpotModel.floor).distinct().all()
    parking_map = []
    
    for floor in floors:
        spots = db.query(ParkingSpotModel).filter(
            ParkingSpotModel.floor == floor[0]
        ).all()
        parking_map.append({
            "floor": floor[0],
            "spots": spots
        })
    
    return parking_map

@router.post("/spots", response_model=ParkingSpot)
def create_parking_spot(
    spot: ParkingSpotCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_spot = ParkingSpotModel(**spot.dict())
    db.add(db_spot)
    db.commit()
    db.refresh(db_spot)
    return db_spot

@router.post("/entry", response_model=ParkingRecord)
def register_entry(
    entry: ParkingRecordCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Verificar se o veículo existe e pertence ao usuário
    vehicle = db.query(VehicleModel).filter(
        VehicleModel.id == entry.vehicle_id,
        VehicleModel.owner_id == current_user.id
    ).first()
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Veículo não encontrado"
        )
    
    # Verificar se a vaga está disponível
    spot = db.query(ParkingSpotModel).filter(
        ParkingSpotModel.id == entry.spot_id,
        ParkingSpotModel.is_occupied == False
    ).first()
    if not spot:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vaga não disponível"
        )
    
    # Registrar entrada
    record = ParkingRecordModel(
        vehicle_id=entry.vehicle_id,
        spot_id=entry.spot_id,
        entry_photo=entry.entry_photo
    )
    
    # Atualizar status da vaga
    spot.is_occupied = True
    spot.current_vehicle_id = entry.vehicle_id
    
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@router.post("/exit/{record_id}", response_model=ParkingRecord)
def register_exit(
    record_id: int,
    exit_photo: str = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Buscar registro
    record = db.query(ParkingRecordModel).join(
        VehicleModel
    ).filter(
        ParkingRecordModel.id == record_id,
        VehicleModel.owner_id == current_user.id,
        ParkingRecordModel.exit_time == None
    ).first()
    
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro de entrada não encontrado"
        )
    
    # Atualizar registro com saída
    record.exit_time = datetime.now()
    record.exit_photo = exit_photo
    
    # Liberar a vaga
    spot = db.query(ParkingSpotModel).filter(
        ParkingSpotModel.id == record.spot_id
    ).first()
    spot.is_occupied = False
    spot.current_vehicle_id = None
    
    db.commit()
    db.refresh(record)
    return record 