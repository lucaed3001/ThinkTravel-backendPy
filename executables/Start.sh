#!/bin/bash
cd ..
# Attiva l'ambiente virtuale
source venv/bin/activate

# Avvia l'app con uvicorn
uvicorn app.main:app --reload
# Info per l'utente
# Questo script viene usato per avviare l'applicazione.
# Deve essere eseguito dopo aver eseguito 'FirstStart.sh' per impostare l'ambiente virtuale e installare i pacchetti richiesti.
