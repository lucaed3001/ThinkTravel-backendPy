import threading
import time
import logging
from googletrans import Translator
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.hotel import Hotel, HotelTranslation

# Lingue supportate per la traduzione
LANGUAGES = ['it', 'de', 'zh-cn', 'fr', 'es']

# Configurazione del logging
#logging.basicConfig(level=print, format='%(asctime)s - %(message)s', filename='translation_worker.log')

def translate_text(text, target_lang, translator):
    try:
        # Traduci il testo nella lingua di destinazione
        return translator.translate(text, dest=target_lang).text
    except Exception as e:
        print(f"Errore nella traduzione per la lingua {target_lang}: {e}")
        return text

def translation_worker():
    print("Avvio del worker di traduzione...")
    
    while True:
        db: Session = SessionLocal()  # Crea una sessione con il database
        translator = Translator()  # Crea un oggetto traduttore
        print("Inizio del ciclo di traduzione...")

        try:
            # Per ogni lingua nel vettore LANGUAGES, cerchiamo solo gli hotel che non sono tradotti in quella lingua
            for lang in LANGUAGES:
                hotels_to_translate = db.query(Hotel) \
                    .outerjoin(HotelTranslation, (Hotel.id == HotelTranslation.hotel_id) & (HotelTranslation.lang == lang)) \
                    .filter(HotelTranslation.id == None) \
                    .all()


                if not hotels_to_translate:
                    print(f"Nessun hotel da tradurre per la lingua {lang}.")
                
                for hotel in hotels_to_translate:
                    print(f"Traduzione mancante per hotel {hotel.id} in lingua '{lang}', inizio traduzione...")

                    # Traduci la descrizione dell'hotel nella lingua
                    translated_desc = translate_text(hotel.description, lang, translator)

                    # Crea un nuovo oggetto per la traduzione
                    translation = HotelTranslation(
                        hotel_id=hotel.id,
                        lang=lang,  # Usa il codice lingua, es. 'it', 'en', 'de', ecc.
                        description=translated_desc
                    )

                    # Aggiungi e committa la traduzione nel DB
                    db.add(translation)
                    db.commit()
                    print(f"Traduzione completata per hotel {hotel.id} in lingua '{lang}'.")

        except Exception as e:
            print(f"Errore nel worker: {e}")
        finally:
            db.close()  # Chiudi la sessione del DB

        # Fai dormire il thread per 30 minuti (1800 secondi)
        time.sleep(1800)  # Esegui ogni 30 minuti (1800 secondi)
        print("Fine del ciclo di traduzione, attendo 30 minuti...")

# Avvio del thread di traduzione
def start_translation_worker():
    translation_thread = threading.Thread(target=translation_worker)
    translation_thread.daemon = True  # Impostiamo il thread come 'daemon' per terminare con il programma
    translation_thread.start()

    print("Worker di traduzione avviato in un thread separato.")

# Esegui l'avvio del worker
#start_translation_worker()

