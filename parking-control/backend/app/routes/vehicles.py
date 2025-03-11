from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.schemas import VehicleCreate, Vehicle, VehicleWithOwner
from app.models.models import Vehicle as VehicleModel
from app.utils.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=Vehicle)
def create_vehicle(
    vehicle: VehicleCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_vehicle = VehicleModel(
        **vehicle.dict(),
        owner_id=current_user.id
    )
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

@router.get("/", response_model=List[VehicleWithOwner])
def read_vehicles(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    vehicles = db.query(VehicleModel).filter(
        VehicleModel.owner_id == current_user.id
    ).offset(skip).limit(limit).all()
    return vehicles

@router.get("/{vehicle_id}", response_model=VehicleWithOwner)
def read_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    vehicle = db.query(VehicleModel).filter(
        VehicleModel.id == vehicle_id,
        VehicleModel.owner_id == current_user.id
    ).first()
    if vehicle is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Veículo não encontrado"
        )
    return vehicle

@router.delete("/{vehicle_id}")
def delete_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    vehicle = db.query(VehicleModel).filter(
        VehicleModel.id == vehicle_id,
        VehicleModel.owner_id == current_user.id
    ).first()
    if vehicle is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Veículo não encontrado"
        )
    db.delete(vehicle)
    db.commit()
    return {"message": "Veículo removido com sucesso"} 