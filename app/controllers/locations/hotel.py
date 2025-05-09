from app.models import Hotel, Organizator
from sqlalchemy.orm import Session, joinedload
from app.schemas import HotelSchema, HotelFullSchema, CitySchema, OrgSchema, CountrySchema, CurrencySchema
from app.controllers.locations import get_city_by_id
from app.controllers.auth import get_org_by_id
from sqlalchemy.sql import func
from googletrans import Translator

translator = Translator()

def get_all_hotels(db: Session):
    try:
        hotels = db.query(Hotel).all()

        return [HotelSchema.model_validate(hotel) for hotel in hotels]
    except Exception as e:
        raise Exception(f"Error fetching hotels: {str(e)}")


    except Exception as e:
        raise Exception(f"Error fetching all hotels: {str(e)}")
    
def get_hotel_by_id(db: Session, id: int, lang: str = "en"):
    try:
        hotel = db.query(Hotel).filter(Hotel.id == id).first()
        if not hotel:
            raise ValueError("Hotel not found")

        city_obj = get_city_by_id(db, hotel.city, lang=lang)
        org_obj = get_org_by_id(db, hotel.organizer)
        

        hotel_data = {
            "id": hotel.id,
            "name": hotel.name,
            "address": hotel.address,
            "city": CitySchema.model_validate(city_obj) if city_obj else None,
            "description": translator.translate(hotel.description, dest=lang).text if lang != "en" else hotel.description,
            "graduation": hotel.graduation,
            "organizer": OrgSchema.model_validate(org_obj) if org_obj else None,
            "star_number": hotel.star_number,
        }

        return HotelFullSchema.model_validate(hotel_data)

    except Exception as e:
        raise Exception(f"Error fetching hotel: {str(e)}")
    

def get_suggested_hotels(db: Session, n: int = 10, lang: str = "en"):
    try:
        # Recupera n hotel casuali direttamente dal database
        hotels = db.query(Hotel).order_by(func.random()).limit(n).all()

        if not hotels:
            raise ValueError("No hotels found in the database")

        # Prepara i dati per la risposta
        hotels_data = []
        for hotel in hotels:
            city_obj = get_city_by_id(db, hotel.city, lang=lang)
            org_obj = get_org_by_id(db, hotel.organizer)

            hotel_data = {
                "id": hotel.id,
                "name": hotel.name,
                "address": hotel.address,
                "city": CitySchema.model_validate(city_obj) if city_obj else None,
                "description": translator.translate(hotel.description, dest=lang).text if lang != "en" else hotel.description,
                "graduation": hotel.graduation,
                "organizer": OrgSchema.model_validate(org_obj) if org_obj else None,
                "star_number": hotel.star_number,
            }

            hotels_data.append(HotelFullSchema.model_validate(hotel_data))

        return hotels_data
    except Exception as e:
        raise Exception(f"Error fetching suggested hotels: {str(e)}")
    


