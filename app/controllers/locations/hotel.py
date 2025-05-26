import shutil
from app.models import Hotel, Organizator, City, HotelTranslation, Country, Currency
from sqlalchemy.orm import Session, joinedload
from app.schemas import HotelSchema, HotelFullSchema, CitySchema, OrgSchema, CountrySchema, CurrencySchema, HotelCreate
from app.controllers.locations import get_city_by_id
from app.controllers.auth import get_org_by_id
from sqlalchemy.sql import func, or_
from googletrans import Translator
import os
import re
from fastapi import File, HTTPException, UploadFile, status
from pathlib import Path

translator = Translator()

def get_all_hotels(db: Session, lang: str = "en"):
    try:
        hotels = db.query(Hotel).options(
            joinedload(Hotel.translations)
        ).all()

        hotel_list = []

        for hotel in hotels:
            translation = next((t for t in hotel.translations if t.lang == lang), None)

            hotel_list.append({
                'id': hotel.id,
                'name': hotel.name,
                'address': hotel.address,
                'city': hotel.city,  # Puoi arricchirlo se vuoi anche nome città tradotto
                'description': translation.description if translation and translation.description else hotel.description,
                'graduation': hotel.graduation,
                'organizer': hotel.organizer,
                'star_number': hotel.star_number
            })

        return hotel_list

    except Exception as e:
        raise Exception(f"Error fetching hotels: {str(e)}")


    except Exception as e:
        raise Exception(f"Error fetching all hotels: {str(e)}")
    

def get_hotel_by_id(db: Session, id: int, lang: str = "en"):
    try:
        print(f"Fetching hotel with ID: {id} and language: {lang}")
        # Esegui la query per ottenere l'hotel con le relative traduzioni
        hotel = (
            db.query(Hotel)
            .outerjoin(Hotel.translations)
            .outerjoin(City)
            .outerjoin(Organizator)
            .filter(Hotel.id == id)
            .first()
        )

        print(f"Hotel found: {hotel}")
        if not hotel:
            raise ValueError("Hotel not found")

        # Cerca la traduzione per la lingua richiesta, se non presente utilizza quella in inglese
        translation = next((t for t in hotel.translations if t.lang == lang.upper()), None)
        if lang != "en" and not translation:
            raise ValueError("Translation not found for the requested language")

        # Carica la città tradotta
        city_obj = get_city_by_id(db, hotel.city, lang=lang)

        # Carica l'organizzatore
        org_obj = get_org_by_id(db, hotel.organizer)

        hotel_data = {
            "id": hotel.id,
            "name": hotel.name,
            "address": hotel.address,
            "city": CitySchema.model_validate(city_obj) if city_obj else None,
            "description": translation.description if translation and translation.description else hotel.description,
            "graduation": hotel.graduation,
            "organizer": OrgSchema.model_validate(org_obj) if org_obj else None,
            "star_number": hotel.star_number,
        }

        return HotelFullSchema.model_validate(hotel_data)

    except Exception as e:
        raise Exception(f"Error fetching hotel: {str(e)}")

def get_suggested_hotels(db: Session, n: int = 10, lang: str = "en"):
    try:
        print(f"Fetching {n} suggested hotels with language: {lang}")

        # Costruiamo la query con eager loading delle relazioni
        query = db.query(Hotel).options(
            joinedload(Hotel.translations),
            joinedload(Hotel.city_rel),      # Usa la relazione vera (non la colonna city)
            joinedload(Hotel.organizer_rel)
        )

        # Se la lingua non è inglese, filtra hotel che hanno una traduzione in quella lingua
        if lang != "en":
            query = query.join(Hotel.translations).filter(HotelTranslation.lang == lang)

        # Estrai N hotel casuali
        hotels = query.order_by(func.random()).limit(n).all()

        if not hotels:
            raise ValueError("No hotels found in the database")

        hotels_list = []

        for hotel in hotels:
            # Cerca la traduzione nella lingua richiesta
            translation = next((t for t in hotel.translations if t.lang == lang), None)

            # Fallback alla traduzione in inglese se non esiste quella richiesta
            if lang != "en" and not translation:
                translation = next((t for t in hotel.translations if t.lang == "en"), None)

            # Carica la città con le sue traduzioni
            city_obj = get_city_by_id(db, hotel.city, lang=lang)

            # Carica l'organizzatore
            org_obj = get_org_by_id(db, hotel.organizer)

            # Prepara i dati dell'hotel
            hotel_data = {
                "id": hotel.id,
                "name": hotel.name,
                "address": hotel.address,
                "city": city_obj,
                "description": translation.description if translation else hotel.description,
                "graduation": hotel.graduation,
                "organizer": org_obj,
                "star_number": hotel.star_number,
            }

            # Validiamo con lo schema Pydantic
            hotels_list.append(HotelFullSchema.model_validate(hotel_data))

        return hotels_list

    except Exception as e:
        raise Exception(f"Error fetching suggested hotels: {str(e)}")


def get_hotels_by_city_name(db: Session, city_name: str, lang: str = "en"):
    try:
        # Cerca la città con il nome esatto (ignorando maiuscole/minuscole)
        city = db.query(City).filter(func.lower(City.name) == city_name.strip().lower()).first()

        return get_hotels_by_city_id(db, int(city.id), lang) if city else []

    except Exception as e:
        raise Exception(f"Error fetching city by name: {str(e)}")

def get_hotels_by_city_id(db: Session, city_id: int, lang: str = "en"):
    try:
        print(f"Fetching hotels for city ID: {city_id} with language: {lang}")

        hotels = (
            db.query(Hotel)
            .options(
                joinedload(Hotel.translations),
                joinedload(Hotel.city_rel),      
                joinedload(Hotel.organizer_rel)  
            )
            .filter(Hotel.city == city_id)
            .all()
        )

        if not hotels:
            raise ValueError(f"No hotels found for city ID {city_id}")

        hotels_list = []

        for hotel in hotels:
            translation = next((t for t in hotel.translations if t.lang == lang.upper()), None)

            if lang != "en" and not translation:
                raise ValueError(f"Translation not found for hotel {hotel.id} in language {lang}")

            hotel_data = {
                "id": hotel.id,
                "name": hotel.name,
                "address": hotel.address,
                "city": hotel.city,  
                "description": translation.description if translation and translation.description else hotel.description,
                "graduation": hotel.graduation,
                "organizer": hotel.organizer, 
                "star_number": hotel.star_number,
            }

            hotels_list.append(HotelSchema.model_validate(hotel_data))

        return hotels_list

    except Exception as e:
        raise Exception(f"Error fetching hotels by city ID: {str(e)}")

def get_hotel_images(id, n_max):
    cartella = "app/static/images/hotels"
    immagini = []
    immagini_altre = []
    id_str = str(id)

    try:
        if not os.path.exists(cartella):
            raise FileNotFoundError(f"La cartella '{cartella}' non esiste.")

        for filename in os.listdir(cartella):
            if re.match(rf"^{re.escape(id_str)}-\d+\..+$", filename):
                if re.match(rf"^{re.escape(id_str)}-1\..+$", filename):
                    immagini.insert(0, os.path.join(filename))  # Prima posizione
                else:
                    immagini_altre.append(os.path.join(filename))

        immagini += immagini_altre

        if not immagini:
            raise FileNotFoundError(f"Nessuna immagine trovata per la città con ID '{id}'.")

        return immagini[:n_max]

    except Exception as e:
        print(f"Errore durante la ricerca delle immagini: {e}")
        return []


def add_hotel(db: Session, hotel_data: HotelCreate):
    try:
        # Crea il nuovo hotel
        new_hotel = Hotel(
            name=hotel_data.name,
            address=hotel_data.address,
            city=hotel_data.city,
            description=hotel_data.description,
            graduation=None,
            organizer=hotel_data.organizer,
            star_number=hotel_data.star_number,
        )

        db.add(new_hotel)
        db.commit()
        db.refresh(new_hotel)

        return new_hotel  # ← Oggetto conforme a HotelSchema

    except Exception as e:
        db.rollback()
        raise Exception(f"Error adding hotel: {str(e)}")


def delete_hotel(db: Session, hotel_id: int, current_org: int):
    try:
        # Cerca l'hotel nel database
        hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
        if not hotel:
            raise HTTPException(status_code=404, detail="Hotel not found")

        # Controlla se l'utente è l'organizzatore dell'hotel
        print(f"Current user: {current_org}")
        print(f"Hotel organizer: {hotel.organizer}")
        if hotel.organizer != current_org:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not the owner of this hotel"
            )

        # Cancella l'hotel
        db.delete(hotel)
        db.commit()

        return {"message": "Hotel deleted successfully"}

    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting hotel: {str(e)}"
        )

def put_hotel_images(db: Session, files: list[UploadFile] = File(...), token: str = None, id: int = 0):
    try:
        save_dir = Path("app/static/images/hotels")
        save_dir.mkdir(parents=True, exist_ok=True)

        saved_files = []
        saved_files.extend(get_hotel_images(id, 10))

        for file in files:
            original_extension = os.path.splitext(file.filename)[1]
            if original_extension.lower() not in [".jpg", ".jpeg", ".png", ".gif"]:
                raise HTTPException(status_code=400, detail=f"Formato file non supportato: {file.filename}")

            # Generate a unique filename for each image
            file_index = len(saved_files) + 1
            file_path = save_dir / f"{id}-{file_index}{original_extension.lower()}"

            # Save the file
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            saved_files.append(file_path.name)

        return {"filenames": saved_files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

def get_suggested_hotels_by_country(db: Session, country_id: int, n=10, lang="en"):
    try:
        print(f"Fetching {n} suggested hotels in country_id={country_id} with language: {lang}")

        hotels = db.query(Hotel).options(
            joinedload(Hotel.translations),
            joinedload(Hotel.city_rel).joinedload(City.translations),
            joinedload(Hotel.city_rel).joinedload(City.country_rel).joinedload(Country.translations),
            joinedload(Hotel.organizer_rel)
        ).filter(
            Hotel.city_rel.has(City.country == country_id)
        ).order_by(
            func.random()
        ).limit(n).all()

        if not hotels:
            raise ValueError(f"No hotels found for country_id: {country_id}")

        suggested_hotels = []

        for hotel in hotels:
            hotel_translation = next((t for t in hotel.translations if t.lang == lang), None)
            if lang != "en" and not hotel_translation:
                hotel_translation = next((t for t in hotel.translations if t.lang == "en"), None)

            city = hotel.city_rel
            city_translation = next((t for t in city.translations if t.lang == lang), None)
            country = city.country_rel
            country_translation = next((t for t in country.translations if t.lang == lang), None)

            city_obj = {
                "id": city.id,
                "name": city_translation.name if city_translation and city_translation.name else city.name
            }

            country_obj = {
                "id": country.ID,
                "name": country_translation.name if country_translation and country_translation.name else country.name
            }

            organizer_obj = get_org_by_id(db, hotel.organizer)

            hotel_data = {
                "id": hotel.id,
                "name": hotel.name,
                "description": hotel_translation.description if hotel_translation and hotel_translation.description else hotel.description,
                "address": hotel.address,
                "city": {**city_obj, "country": country_obj},
                "star_number": hotel.star_number,
                "graduation": hotel.graduation,
                "organizer": organizer_obj,
            }

            suggested_hotels.append(HotelFullSchema.model_validate(hotel_data))

        return suggested_hotels

    except Exception as e:
        raise Exception(f"Error fetching suggested hotels by country: {str(e)}")
