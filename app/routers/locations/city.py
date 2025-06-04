from fastapi import APIRouter, HTTPException, Depends
from app.controllers.locations import get_suggested_cities_by_country, get_all_cities, get_city_by_id, get_city_images, get_suggested_cities, get_cities_by_partial_name
from app.database import get_db
from sqlalchemy.orm import Session
from app.schemas import CitySchema, CityCreate
from typing import Optional

router = APIRouter()

@router.get("/", response_model=list[CitySchema])
async def get_all_countries_route(db: Session = Depends(get_db), q: Optional[str] = "", lang: Optional[str] = "en"): 
    try:
        if(q == ""):
            cities = get_all_cities(db, lang.upper())
        else:
            cities = get_cities_by_partial_name(db, q, lang.upper())
        if not cities:
            raise ValueError("No cities found")
        return cities
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{id}", response_model=CitySchema)
async def get_country_by_id_route(id: int, db: Session = Depends(get_db), lang: Optional[str] = "en"):
    try:
        country = get_city_by_id(db, id, lang.upper()) 
        return country
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/images/{id}")
async def get_city_image_f(id: int, db: Session = Depends(get_db)):
    return get_city_images(id=id, n_max=10)

@router.get("/suggested/{n}", response_model=list[CitySchema])
async def get_suggested_cities_route(n: int, db: Session = Depends(get_db), lang: Optional[str] = "en", country_id: Optional[int] = None):
    try:
        if not country_id:
            cities = get_suggested_cities(db, n, lang.upper()) 
        else:
            cities = get_suggested_cities_by_country(db=db, country_id=country_id, n=n, lang=lang.upper()) # Chiama la funzione del controller con db come parametro
        return cities[:n]  # Restituisce solo i primi n risultati
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

