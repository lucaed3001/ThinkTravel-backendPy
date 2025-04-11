#!/bin/bash
cd ..
# Crea l'ambiente virtuale
python3 -m venv venv

# Attiva l'ambiente virtuale
source venv/bin/activate

# Installa i pacchetti richiesti
pip install -r requirements.txt

# Disattiva l'ambiente virtuale
deactivate

echo "✅ First start complete. You can now run the program using './start.sh'."
# Info per l'utente
# Questo script viene usato per impostare l'ambiente virtuale e installare i pacchetti richiesti.
# Deve essere eseguito solo una volta, al primo avvio del programma.
# Dopo, puoi usare './start.sh' per avviare il programma.
