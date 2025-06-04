from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Currency(Base):
    __tablename__ = "currency"

    ID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    simbol = Column(String(1), nullable=True)  # Il simbolo può essere NULL

    rooms = relationship("Room", back_populates="currency_ref")
