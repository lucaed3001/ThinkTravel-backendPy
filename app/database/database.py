import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Carica le variabili d'ambiente
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Crea l'engine di SQLAlchemy per MySQL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency per ottenere una sessione DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
