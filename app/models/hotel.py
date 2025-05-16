from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Hotel(Base):
    __tablename__ = 'hotels'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=True)
    address = Column(String(255), nullable=True)
    city = Column(Integer, ForeignKey('cities.id'), nullable=True)
    description = Column(Text, nullable=True)
    graduation = Column(Integer, nullable=True)
    organizer = Column(Integer, ForeignKey('organizers.id'), nullable=True)
    star_number = Column(Integer, nullable=True)

    city_rel = relationship("City", back_populates="hotels")
    organizer_rel = relationship("Organizator", back_populates="hotels")
    translations = relationship('HotelTranslation', back_populates='hotel', lazy='select', cascade="all, delete-orphan")

class HotelTranslation(Base):
    __tablename__ = 'hotel_translations'

    id = Column(Integer, primary_key=True, index=True)  # ID unico per ogni traduzione
    hotel_id = Column(Integer, ForeignKey('hotels.id'), nullable=False)  # ID dell'hotel (chiave esterna)
    lang = Column(String, nullable=False)  # Codice lingua (ad es. 'it', 'en', 'de', ecc.)
    description = Column(String, nullable=True)  # Descrizione tradotta dell'hotel

    # Relazione con la tabella Hotel
    hotel = relationship('Hotel', back_populates='translations')

