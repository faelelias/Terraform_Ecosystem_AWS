from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    apartment: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Vehicle Schemas
class VehicleBase(BaseModel):
    plate: str
    model: str
    color: str
    year: int

class VehicleCreate(VehicleBase):
    pass

class Vehicle(VehicleBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Parking Spot Schemas
class ParkingSpotBase(BaseModel):
    number: str
    floor: str

class ParkingSpotCreate(ParkingSpotBase):
    pass

class ParkingSpot(ParkingSpotBase):
    id: int
    is_occupied: bool
    current_vehicle_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True

# Parking Record Schemas
class ParkingRecordBase(BaseModel):
    vehicle_id: int
    spot_id: int

class ParkingRecordCreate(ParkingRecordBase):
    entry_photo: Optional[str] = None

class ParkingRecord(ParkingRecordBase):
    id: int
    entry_time: datetime
    exit_time: Optional[datetime] = None
    entry_photo: Optional[str] = None
    exit_photo: Optional[str] = None

    class Config:
        from_attributes = True

# Response Schemas
class ParkingMapResponse(BaseModel):
    floor: str
    spots: List[ParkingSpot]

class VehicleWithOwner(Vehicle):
    owner: User

class ParkingSpotWithVehicle(ParkingSpot):
    vehicle: Optional[Vehicle] = None 