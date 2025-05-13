from app.models import Hotel, Organizator, City, HotelTranslation, Country, Currency
from sqlalchemy.orm import Session, joinedload
from app.schemas import HotelSchema, HotelFullSchema, CitySchema, OrgSchema, CountrySchema, CurrencySchema
from app.controllers.locations import get_city_by_id
from app.controllers.auth import get_org_by_id
from sqlalchemy.sql import func, or_
from googletrans import Translator

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
        if lang == "en":
            # Se la lingua è inglese, non uniamo la tabella delle traduzioni.
            hotels = db.query(Hotel).join(City).join(Organizator).order_by(func.random()).limit(n).all()
        else:
            # Se la lingua non è inglese, recuperiamo con la traduzione
            hotels = db.query(Hotel).join(Hotel.translations).join(City).join(Organizator).filter(HotelTranslation.lang == lang).order_by(func.random()).limit(n).all()

        if not hotels:
            raise ValueError("No hotels found in the database")

        # Prepara i dati per la risposta
        hotels_data = []
        for hotel in hotels:
            if lang == "en":
                # Se la lingua è inglese, usa i dati direttamente dalla tabella hotels
                translation = None
            else:
                # Cerca la traduzione per la lingua richiesta
                translation = next((t for t in hotel.translations if t.lang == lang), None)
                if lang != "en" and not translation:
                    # Se non trovi la traduzione per la lingua, usa quella in inglese
                    translation = next((t for t in hotel.translations if t.lang == "en"), None)

            # Carica la città tradotta
            city_obj = get_city_by_id(db, hotel.city, lang=lang)

            # Carica l'organizzatore
            org_obj = get_org_by_id(db, hotel.organizer)

            hotel_data = {
                "id": hotel.id,
                "name": hotel.name,  # Nome dell'hotel non tradotto
                "address": hotel.address,
                "city": CitySchema.model_validate(city_obj) if city_obj else None,
                "description": translation.description if translation and translation.description else hotel.description,
                "graduation": hotel.graduation,
                "organizer": OrgSchema.model_validate(org_obj) if org_obj else None,
                "star_number": hotel.star_number,
            }

            hotels_data.append(HotelFullSchema.model_validate(hotel_data))

        return hotels_data

    except Exception as e:
        raise Exception(f"Error fetching suggested hotels: {str(e)}")






    


