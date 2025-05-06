from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Organizator(Base):
    __tablename__ = "organizers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    address = Column(String(255), nullable=True)
    city = Column(Integer, ForeignKey("cities.id"), nullable=False)
    phone = Column(String(20), nullable=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    vat = Column(String(20), nullable=True)

    city_rel = relationship("City", back_populates="organizers")

    hotels = relationship("Hotel", back_populates="organizer_rel")
