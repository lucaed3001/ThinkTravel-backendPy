from fastapi import APIRouter, HTTPException, Depends
from app.controllers.locations import *
from app.database import get_db
from sqlalchemy.orm import Session
from app.schemas import HotelSchema, HotelFullSchema, HotelCreate
from typing import Dict, Optional
from app.controllers.lib import verify_token
from app.routers.auth import oauth2_org_scheme


router = APIRouter()

@router.get("/", response_model=list[HotelSchema])
async def get_all_countries_route(db: Session = Depends(get_db), lang: Optional[str] = "en", cid: Optional[int] = None, cname: Optional[str] = ""):  # Passa la sessione come dipendenza
    try:
        if(cid == None and cname == ""):
            hotels = get_all_hotels(db, lang=lang.upper()) 
        elif cid != None and cname == "":
            hotels = get_hotels_by_city_id(db, city_id=cid ,lang=lang.upper())
        elif cid == None and cname != "":
            hotels = get_hotels_by_city_name(db, lang=lang.upper(), city_name=cname)
        return hotels
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/{id}", response_model=HotelFullSchema)
async def get_hotel_by_id_route(id: int, db: Session = Depends(get_db), lang: Optional[str] = "en"):
    try:
        hotel = get_hotel_by_id(db, id, lang=lang.upper()) 
        return hotel
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/images/{id}", response_model=list[str])
async def get_hotel_images_route(id: int, n_max: Optional[int] = 10):
    try:
        images = get_hotel_images(id, n_max)
        return images
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
@router.get("/suggested/{n}", response_model=list[HotelFullSchema])
async def get_suggested_cities_route(n: int, db: Session = Depends(get_db), lang: Optional[str] = "en", country_id: Optional[int] = None):
    try:
        if not country_id:
            hotels = get_suggested_hotels(db, n, lang.upper())  # Chiama la funzione del controller con db come parametro
        else:
            hotels = get_suggested_hotels_by_country(db=db, country_id=country_id, n=n, lang=lang.upper()) # Chiama la funzione del controller con db come parametro
        
        return hotels[:n]  
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/suggested/{n}", response_model=list[CitySchema])
async def get_suggested_cities_route(n: int, db: Session = Depends(get_db), lang: Optional[str] = "en", country_id: Optional[int] = None):
    try:
        if not country_id:
            cities = get_suggested_cities(db, n, lang.upper())  # Chiama la funzione del controller con db come parametro
        else:
            cities = get_suggested_cities_by_country(db=db, country_id=country_id, n=n, lang=lang.upper()) # Chiama la funzione del controller con db come parametro
        return cities[:n]  # Restituisce solo i primi n risultati
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
        

@router.post("/", response_model=HotelSchema)
async def create_hotel_route(hotel: HotelCreate, db: Session = Depends(get_db)):
    try:
        new_hotel = add_hotel(db, hotel)
        return new_hotel
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@router.delete("/{hotel_id}")
async def delete_hotel_route(
    hotel_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_org_scheme)
):
    try:
        payload = verify_token(token)
        org_id = payload.get("id")
        if not id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        result = delete_hotel(db, hotel_id, org_id)
        return {"message": result["message"]}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error deleting hotel: {str(e)}")

@router.post("/upload-images/{id}")
async def upload_images(
    id: int,
    files: list[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    try:
        if id is None:
            raise HTTPException(status_code=400, detail="Hotel ID is required")

        saved_files = put_hotel_images(db, files=files, id=id)
        return {"uploaded_files": saved_files["filenames"]}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading images: {str(e)}")
    
@router.get("/delete-image/{image_name}")
async def delete_image(
    image_name: str,
    db: Session = Depends(get_db)
):
    try:
        if image_name is None:
            raise HTTPException(status_code=400, detail="Image ID is required")

        result = delete_hotel_image(db, image_name=image_name)
        return {"message": result["message"]}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting image: {str(e)}")
