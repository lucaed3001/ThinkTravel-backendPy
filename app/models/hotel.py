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
