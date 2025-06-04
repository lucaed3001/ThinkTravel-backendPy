from sqlalchemy import Column, Integer, String, Text, DECIMAL, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base  # Assicurati che questo punti correttamente alla tua dichiarazione Base

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    type = Column(String(100), nullable=True)
    name = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    price = Column(DECIMAL(10, 2), nullable=True)
    currency = Column(Integer, ForeignKey("currency.ID"), nullable=True)
    idHotel = Column(Integer, ForeignKey("hotels.id"), nullable=True)
    guest = Column(Integer, nullable=True)
    tv = Column(Integer, nullable=True)
    balcony = Column(Boolean, nullable=True)
    ac = Column(Boolean, nullable=True)
    size = Column(Integer, nullable=True)
    quantity = Column(Integer, nullable=False)

    # Relazioni
    hotel = relationship("Hotel", back_populates="rooms")
    currency_ref = relationship("Currency", back_populates="rooms")
    translations = relationship("RoomTranslation", back_populates="room", cascade="all, delete-orphan")


class RoomTranslation(Base):
    __tablename__ = "room_translations"
    __table_args__ = (
        UniqueConstraint('room_id', 'lang', name='unique_translation'),
    )

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    room_id = Column(Integer, ForeignKey("rooms.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    lang = Column(String(10), nullable=False)
    name = Column(String, nullable=True) 
    description = Column(Text, nullable=True)

    room = relationship("Room", back_populates="translations")