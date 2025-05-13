from app.models import City, Country, CityTranslation
from sqlalchemy.orm import Session, joinedload
import os
import re
from sqlalchemy.sql import or_, func
from googletrans import Translator

translator = Translator()

from sqlalchemy.orm import joinedload

def get_all_cities(db: Session, lang: str):
    try:
        # Carichiamo anche le traduzioni della città e della country
        cities = db.query(City).options(
            joinedload(City.translations),
            joinedload(City.country_rel).joinedload(Country.translations)
        ).all()

        cities_list = []

        for city in cities:
            # Traduzione della città
            city_translation = next((t for t in city.translations if t.lang == lang), None)

            # Traduzione della country
            country = city.country_rel
            country_translation = next((t for t in country.translations if t.lang == lang), None)

            cities_list.append({
                'id': city.id,
                'name': city_translation.name if city_translation and city_translation.name else city.name,
                'description': city_translation.description if city_translation and city_translation.description else city.description,
                'country': {
                    'id': country.ID,
                    'name': country_translation.name if country_translation and country_translation.name else country.name,
                    'description': country_translation.description if country_translation and country_translation.description else country.description,
                },
            })

        return cities_list

    except Exception as e:
        raise Exception(f"Error fetching cities: {str(e)}")




def get_city_by_id(db: Session, id: int, lang: str = "en"):
    try:
        city = db.query(City).options(
            joinedload(City.translations),
            joinedload(City.country_rel).joinedload(Country.translations)
        ).filter(City.id == id).first()

        if city is None:
            raise ValueError("City not found")

        # Traduzione città
        city_translation = next((t for t in city.translations if t.lang == lang), None)

        # Traduzione country
        country = city.country_rel
        country_translation = next((t for t in country.translations if t.lang == lang), None)

        return {
            'id': city.id,
            'name': city_translation.name if city_translation and city_translation.name else city.name,
            'description': city_translation.description if city_translation and city_translation.description else city.description,
            'country': {
                'id': country.ID,
                'name': country_translation.name if country_translation and country_translation.name else country.name,
                'description': country_translation.description if country_translation and country_translation.description else country.description,
            },
        }

    except ValueError as e:
        raise e
    except Exception as e:
        raise Exception(f"Error fetching city by ID: {str(e)}")

def get_city_images(id, n_max):
    cartella = "app/static/images/cities"
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
    
def get_suggested_cities(db: Session, n=10, lang="en"):
    try:
        cities = db.query(City).options(
            joinedload(City.translations),
            joinedload(City.country_rel).joinedload(Country.translations)
        ).order_by(func.random()).limit(n).all()

        suggested_cities = []

        for city in cities:
            city_translation = next((t for t in city.translations if t.lang == lang), None)
            country = city.country_rel
            country_translation = next((t for t in country.translations if t.lang == lang), None)

            suggested_cities.append({
                'id': city.id,
                'name': city_translation.name if city_translation and city_translation.name else city.name,
                'description': city_translation.description if city_translation and city_translation.description else city.description,
                'country': {
                    'id': country.ID,
                    'name': country_translation.name if country_translation and country_translation.name else country.name,
                    'description': country_translation.description if country_translation and country_translation.description else country.description,
                },
            })

        return suggested_cities

    except Exception as e:
        raise Exception(f"Error fetching suggested cities: {str(e)}")
    


def get_cities_by_partial_name(db: Session, partial_name: str, lang: str = "en"):
    try:
        # Trova le città il cui nome o la cui traduzione contiene partial_name
        cities = (
            db.query(City)
            .options(
                joinedload(City.translations),
                joinedload(City.country_rel).joinedload(Country.translations)
            )
            .outerjoin(CityTranslation, (City.id == CityTranslation.city_id) & (CityTranslation.lang == lang))
            .filter(
                or_(
                    func.lower(City.name).ilike(f"%{partial_name.lower()}%"),
                    City.id.in_(
                        db.query(CityTranslation.city_id)
                        .filter(func.lower(CityTranslation.name).ilike(f"%{partial_name.lower()}%"))
                        .subquery()
                    )
                )
            )
            .all()
        )

        if not cities:
            raise ValueError("No cities found with the given name")

        results = []
        for city in cities:
            # Trova la traduzione della città nella lingua richiesta
            city_translation = next((t for t in city.translations if t.lang == lang), None)

            # Trova la traduzione del paese nella lingua richiesta
            country_translation = next((t for t in city.country_rel.translations if t.lang == lang), None)

            results.append({
                'id': city.id,
                'name': city_translation.name if city_translation and city_translation.name else city.name,
                'description': city_translation.description if city_translation and city_translation.description else city.description,
                'country': {
                    'id': city.country_rel.ID,
                    'name': country_translation.name if country_translation and country_translation.name else city.country_rel.name,
                    'description': country_translation.description if country_translation and country_translation.description else city.country_rel.description
                }
            })

        return results

    except Exception as e:
        raise Exception(f"Error fetching cities by partial name: {str(e)}")
