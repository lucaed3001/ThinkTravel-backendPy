from fastapi import APIRouter, HTTPException, Depends
from app.controllers.locations import get_all_countries, get_country_by_id, get_all_countries_names, get_country_images
from app.database import get_db
from sqlalchemy.orm import Session
from app.schemas.country import CountrySchema, CountryOnlyNameSchema

router = APIRouter()

# Route per ottenere tutti i paesi
@router.get("/", response_model=list[CountrySchema])
async def get_all_countries_route(db: Session = Depends(get_db)):  # Passa la sessione come dipendenza
    try:
        countries = get_all_countries(db)  # Chiama la funzione del controller con db come parametro
        return countries
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/names", response_model=list[CountryOnlyNameSchema])
async def get_all_countries_route(db: Session = Depends(get_db)):
    try:
        countries = get_all_countries_names(db)  # Chiama la funzione del controller con db come parametro
        return countries
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Route per ottenere un singolo paese per ID
@router.get("/{id}", response_model=CountrySchema)
async def get_country_by_id_route(id: int, db: Session = Depends(get_db)):
    try:
        country = get_country_by_id(db, id)  # Chiama la funzione del controller
        return country
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/images/{id}")
async def get_country_image_f(id: int, db: Session = Depends(get_db)):
    return get_country_images(id=id, n_max=10)
