from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.models import Country  # Assumendo che il modello `Country` sia definito correttamente
from app.models import Organizator  # Aggiungi questa importazione per Organizator

class City(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    country = Column(Integer, ForeignKey('countries.ID'), nullable=False)  
    description = Column(Text)

    country_rel = relationship("Country", back_populates="cities")

    organizers = relationship('Organizator', back_populates='city_rel')
    
    images = relationship('CityImage', back_populates='city', cascade='all, delete-orphan')

    hotels = relationship("Hotel", back_populates="city_rel")

    translations = relationship('CityTranslation', back_populates='city', lazy='select')


class CityImage(Base):
    __tablename__ = 'city_images'
    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey('cities.id', ondelete='CASCADE'), nullable=False)
    url = Column(String, nullable=False)
    
    city = relationship('City', back_populates='images')


class CityTranslation(Base):
    __tablename__ = "city_translations"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"))
    lang = Column(String, nullable=False)
    name = Column(String)  # <-- Assicurati che questa riga esista
    description = Column(Text)  # <-- E anche questa se usi `description`

    city = relationship('City', back_populates='translations')

