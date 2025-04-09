from app.models import Country
from sqlalchemy.orm import Session

# Funzione sincrona
def get_all_countries(db: Session):
    try:
        countries = db.query(Country).all()  # SQLAlchemy sincrono
        countries_list = []
        for country in countries:
            countries_list.append({
                'ID': country.ID,  # Cambia da 'id' a 'ID' per essere coerente con il modello
                'name': country.name,
                'code': country.code,
                'description': country.description,
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


def get_all_countries_names(db: Session):
    try:
        countries = db.query(Country).all()  # SQLAlchemy sincrono
        countries_list = []
        for country in countries:
            countries_list.append({
                'id': country.ID,  # Cambia da 'id' a 'ID' per essere coerente con il modello
                'name': country.name,
            })
        return countries_list
    except Exception as e:
        raise Exception(f"Error fetching countries: {str(e)}")


def get_country_by_id(db: Session, id: int):
    try:
        country = db.query(Country).filter(Country.ID == id).first()  # Ottiene il paese tramite l'ID
        if country is None:
            raise ValueError("Country not found")
        
        return {
            'id': country.ID,
            'name': country.name,
            'code': country.code,
            'description': country.description,
            'language': country.language.name if country.language else None,  # Verifica se la lingua esiste
            'currency': country.currency_rel.name if country.currency_rel else None,  # Verifica se la valuta esiste
            'currency_symbol': country.currency_rel.simbol if country.currency_rel else None,  # Verifica se la valuta esiste
        }
    except ValueError as e:
        raise e
    except Exception as e:
        raise Exception(f"Error fetching country by ID: {str(e)}")

