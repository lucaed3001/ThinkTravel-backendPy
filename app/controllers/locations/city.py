from app.models import City, Country
from sqlalchemy.orm import Session
import os
import re

def get_all_cities(db: Session):
    try:
        cities = db.query(City).all()
        cities_list = []
        for city in cities:
            cities_list.append({
                'id': city.id,
                'name': city.name,
                'description': city.description,
                'country': {
                    'id': city.country_rel.ID,  # Cambia da 'id' a 'ID' per essere coerente con il modello
                    'name': city.country_rel.name,
                },
            })
        return cities_list
    except Exception as e:
        raise Exception(f"Error fetching cities: {str(e)}")


def get_all_countries_names(db: Session):
    try:
        countries = db.query(City).all()  # SQLAlchemy sincrono
        countries_list = []
        for country in countries:
            countries_list.append({
                'id': country.ID,  # Cambia da 'id' a 'ID' per essere coerente con il modello
                'name': country.name,
            })
        return countries_list
    except Exception as e:
        raise Exception(f"Error fetching countries: {str(e)}")


def get_city_by_id(db: Session, id: int):
    try:
        city = db.query(City).filter(City.id == id).first()
        if city is None:
            raise ValueError("Country not found")
        return {
                'id': city.id,
                'name': city.name,
                'description': city.description,
                'country': {
                    'id': city.country_rel.ID,  # Cambia da 'id' a 'ID' per essere coerente con il modello
                    'name': city.country_rel.name,
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
                    immagini.insert(0, os.path.join(cartella, filename))  # Prima posizione
                else:
                    immagini_altre.append(os.path.join(cartella, filename))

        immagini += immagini_altre

        if not immagini:
            raise FileNotFoundError(f"Nessuna immagine trovata per la città con ID '{id}'.")

        return immagini[:n_max]

    except Exception as e:
        print(f"Errore durante la ricerca delle immagini: {e}")
        return []
