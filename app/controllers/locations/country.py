from app.models import Country, CountryTranslation
from app.models import Currency
from app.schemas import CountrySchema
from sqlalchemy.orm import Session, joinedload
import os
import re

# Funzione sincrona
def get_all_countries(db: Session, lang: str):
    try:
        # Carica tutti i paesi con le loro traduzioni (joinedload per ottimizzare)
        countries = db.query(Country).options(
            joinedload(Country.translations),
            joinedload(Country.language),
            joinedload(Country.currency_rel)
        ).all()

        countries_list = []
        for country in countries:
            # Cerca la traduzione nella lingua richiesta
            translation = next((t for t in country.translations if t.lang == lang), None)

            # Usa il nome/descrizione tradotti se disponibili, altrimenti quelli di default
            translated_name = translation.name if translation and translation.name else country.name
            translated_description = translation.description if translation and translation.description else country.description

            countries_list.append({
                'ID': country.ID,
                'name': translated_name,
                'code': country.code,
                'description': translated_description,
                'language': {
                    'ID': country.language.ID,
                    'name': country.language.name,
                    'code': country.language.code
                },
                'currency': {
                    'ID': country.currency_rel.ID,
                    'name': country.currency_rel.name,
                    'simbol': country.currency_rel.simbol
                }
            })

        return countries_list

    except Exception as e:
        raise Exception(f"Error fetching countries: {str(e)}")


def get_all_countries_names(db: Session, lang: str):
    try:
        # Carica i paesi con le loro traduzioni
        countries = db.query(Country).options(
            joinedload(Country.translations)
        ).all()

        countries_list = []
        for country in countries:
            # Cerca la traduzione nella lingua richiesta
            translation = next((t for t in country.translations if t.lang == lang), None)

            # Usa il nome tradotto se disponibile, altrimenti usa quello originale
            translated_name = translation.name if translation and translation.name else country.name

            countries_list.append({
                'id': country.ID,
                'name': translated_name
            })

        return countries_list

    except Exception as e:
        raise Exception(f"Error fetching country names: {str(e)}")

def get_country_by_id(db: Session, id: int, lang: str) -> CountrySchema:
    try:
        # Usa la sintassi classica con db.query()
        country = db.query(Country).options(
            joinedload(Country.translations),
            joinedload(Country.language),
            joinedload(Country.currency_rel)
        ).filter(Country.ID == id).first()

        if not country:
            raise ValueError(f"Country with ID {id} not found")

        
        translation = next((t for t in country.translations if t.lang == lang), None)

        translated_name = translation.name if translation and translation.name else country.name
        translated_description = translation.description if translation and translation.description else country.description

        
        return CountrySchema(
            ID=country.ID,
            name=translated_name,
            code=country.code,
            description=translated_description,
            language=country.language,    
            currency=country.currency_rel  
        )

    except ValueError as e:
        raise e
    except Exception as e:
        raise Exception(f"Error fetching country by ID: {str(e)}")


def get_country_images(id, n_max):
    cartella = "app/static/images/countries"
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
