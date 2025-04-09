from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.models import Language, Currency
from app.database import Base

class Country(Base):
    __tablename__ = 'countries'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False)
    lang = Column(Integer, ForeignKey('languages.ID'), nullable=False)  # Chiave esterna per languages
    currency = Column(Integer, ForeignKey('currency.ID'), nullable=False)  # Chiave esterna per currencies
    code = Column(String(2), nullable=False)
    description = Column(Text)

    language = relationship('Language', backref='countries', lazy='joined')
    currency_rel = relationship('Currency', backref='countries', lazy='joined')  # La relazione è definita qui


    users = relationship("User", back_populates="country_rel")
    cities = relationship("City", back_populates="country_rel")
    images = relationship('CountryImage', back_populates='country', cascade='all, delete-orphan')
    #secondary_languages = relationship("SecondaryLanguage", back_populates="country")

class CountryImage(Base):
    __tablename__ = 'country_images'
    id = Column(Integer, primary_key=True)
    country_id = Column(Integer, ForeignKey('countries.ID', ondelete='CASCADE'), nullable=False)
    url = Column(String, nullable=False)
    
    country = relationship('Country', back_populates='images')
