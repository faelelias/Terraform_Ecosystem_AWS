from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import uvicorn

from app.database import get_db
from app.models import Base, engine
from app.schemas import VehicleCreate, VehicleResponse, ParkingSpotResponse
from app.routes import vehicle_router, auth_router, parking_router, camera_router

# Criar tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Parking Control API",
    description="API para controle de vagas de estacionamento",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar os domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth_router, prefix="/auth", tags=["Autenticação"])
app.include_router(vehicle_router, prefix="/vehicles", tags=["Veículos"])
app.include_router(parking_router, prefix="/parking", tags=["Estacionamento"])
app.include_router(camera_router, prefix="/camera", tags=["Câmeras"])

@app.get("/")
def read_root():
    return {"message": "Bem-vindo ao sistema de controle de estacionamento"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 