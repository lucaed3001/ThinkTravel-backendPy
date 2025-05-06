from fastapi import APIRouter, HTTPException, Depends
from app.controllers.locations import get_all_cities, get_city_by_id, get_city_images, get_suggested_cities
from app.database import get_db
from sqlalchemy.orm import Session
from app.schemas import CitySchema, CityCreate

router = APIRouter()

# Route per ottenere tutti i paesi
@router.get("/", response_model=list[CitySchema])
async def get_all_countries_route(db: Session = Depends(get_db)):  # Passa la sessione come dipendenza
    try:
        countries = get_all_cities(db)  # Chiama la funzione del controller con db come parametro
        return countries
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Route per ottenere un singolo paese per ID
@router.get("/{id}", response_model=CitySchema)
async def get_country_by_id_route(id: int, db: Session = Depends(get_db)):
    try:
        country = get_city_by_id(db, id)  # Chiama la funzione del controller
        return country
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/images/{id}")
async def get_city_image_f(id: int, db: Session = Depends(get_db)):
    return get_city_images(id=id, n_max=10)

@router.get("/suggested/{n}", response_model=list[CitySchema])
async def get_suggested_cities_route(n: int, db: Session = Depends(get_db)):
    try:
        cities = get_suggested_cities(db)  # Chiama la funzione del controller con db come parametro
        return cities[:n]  # Restituisce solo i primi n risultati
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
