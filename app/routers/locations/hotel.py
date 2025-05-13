from fastapi import APIRouter, HTTPException, Depends
from app.controllers.locations import get_all_hotels, get_hotel_by_id, get_suggested_hotels
from app.database import get_db
from sqlalchemy.orm import Session
from app.schemas import HotelSchema, HotelFullSchema
from typing import Optional

router = APIRouter()

# Route per ottenere tutti i paesi
@router.get("/", response_model=list[HotelSchema])
async def get_all_countries_route(db: Session = Depends(get_db), lang: Optional[str] = "en"):  # Passa la sessione come dipendenza
    try:
        hotels = get_all_hotels(db, lang=lang.upper())  # Chiama la funzione del controller con db come parametro
        return hotels
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/{id}", response_model=HotelFullSchema)
async def get_hotel_by_id_route(id: int, db: Session = Depends(get_db), lang: Optional[str] = "en"):
    try:
        hotel = get_hotel_by_id(db, id, lang=lang.upper())  # Chiama la funzione del controller
        return hotel
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/suggested/{n}", response_model=list[HotelFullSchema])
async def get_suggested_cities_route(n: int, db: Session = Depends(get_db), lang: Optional[str] = "en"):
    try:
        hotels = get_suggested_hotels(db, lang=lang.upper())  # Chiama la funzione del controller con db come parametro
        return hotels[:n]  # Restituisce solo i primi n risultati
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
