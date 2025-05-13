import threading
import time
import logging
from googletrans import Translator
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Hotel, HotelTranslation, City, CityTranslation, Country, CountryTranslation, Language

# Lingue supportate per la traduzione
LANGUAGES = []

# Configurazione del logging
#logging.basicConfig(level=print, format='%(asctime)s - %(message)s', filename='translation_worker.log')

def translate_text(text, target_lang, translator):
    try:
        # Traduci il testo nella lingua di destinazione
        return translator.translate(text, dest=target_lang).text
    except Exception as e:
        print(f"[TranslationWorker]Errore nella traduzione per la lingua {target_lang}: {e}")
        return text

def get_languages(db: Session):
    return [lang.code for lang in db.query(Language).all()]

def translation_worker():
    print("[TranslationWorker]Avvio del worker di traduzione...")

    while True:
        db: Session = SessionLocal()
        translator = Translator()
        print("[TranslationWorker]Inizio del ciclo di traduzione...")

        LANGUAGES = get_languages(db)

        try:
            for lang in LANGUAGES:
                # === HOTEL TRANSLATIONS ===
                hotels_to_translate = db.query(Hotel) \
                    .outerjoin(HotelTranslation, (Hotel.id == HotelTranslation.hotel_id) & (HotelTranslation.lang == lang)) \
                    .filter(HotelTranslation.id == None) \
                    .all()

                for hotel in hotels_to_translate:
                    print(f"[TranslationWorker][Hotel] Traduzione mancante per hotel {hotel.id} in lingua '{lang}'")
                    translated_desc = translate_text(hotel.description, lang, translator)

                    translation = HotelTranslation(
                        hotel_id=hotel.id,
                        lang=lang,
                        description=translated_desc
                    )
                    db.add(translation)
                    db.commit()

                # === CITY TRANSLATIONS ===
                cities_to_translate = db.query(City) \
                    .outerjoin(CityTranslation, (City.id == CityTranslation.city_id) & (CityTranslation.lang == lang)) \
                    .filter(CityTranslation.id == None) \
                    .all()

                for city in cities_to_translate:
                    print(f"[TranslationWorker][City] Traduzione mancante per città {city.id} in lingua '{lang}'")
                    translated_name = translate_text(city.name, lang, translator)
                    translated_desc = translate_text(city.description, lang, translator)

                    translation = CityTranslation(
                        city_id=city.id,
                        lang=lang,
                        name=translated_name,
                        description=translated_desc
                    )
                    db.add(translation)
                    db.commit()

                # === COUNTRY TRANSLATIONS ===
                countries_to_translate = db.query(Country) \
                    .outerjoin(CountryTranslation, (Country.ID == CountryTranslation.country_id) & (CountryTranslation.lang == lang)) \
                    .filter(CountryTranslation.id == None) \
                    .all()

                for country in countries_to_translate:
                    print(f"[TranslationWorker][Country] Traduzione mancante per paese {country.ID} in lingua '{lang}'")
                    translated_name = translate_text(country.name, lang, translator)
                    translated_desc = translate_text(country.description, lang, translator)

                    translation = CountryTranslation(
                        country_id=country.ID,
                        lang=lang,
                        name=translated_name,
                        description=translated_desc
                    )
                    db.add(translation)
                    db.commit()

                """# === ROOM TRANSLATIONS ===
                rooms_to_translate = db.query(Room) \
                    .outerjoin(RoomTranslation, (Room.id == RoomTranslation.room_id) & (RoomTranslation.lang == lang)) \
                    .filter(RoomTranslation.id == None) \
                    .all()

                for room in rooms_to_translate:
                    print(f"[TranslationWorker][Room] Traduzione mancante per stanza {room.id} in lingua '{lang}'")
                    translated_desc = translate_text(room.description, lang, translator)

                    translation = RoomTranslation(
                        room_id=room.id,
                        lang=lang,
                        description=translated_desc
                    )
                    db.add(translation)
                    db.commit()"""

        except Exception as e:
            print(f"[TranslationWorker]Errore nel worker: {e}")
        finally:
            db.close()

        print("[TranslationWorker]Fine del ciclo di traduzione, attendo 30 minuti...")
        time.sleep(1800)

# Avvio del thread di traduzione
def start_translation_worker():
    translation_thread = threading.Thread(target=translation_worker)
    translation_thread.daemon = True  # Impostiamo il thread come 'daemon' per terminare con il programma
    translation_thread.start()

    print("[TranslationWorker]Worker di traduzione avviato in un thread separato.")

# Esegui l'avvio del worker
#start_translation_worker()

