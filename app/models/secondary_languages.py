from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.models import Country, Language

class SecondaryLanguage(Base):
    __tablename__ = 'secondary_languages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    country_id = Column(Integer, ForeignKey('countries.ID'), nullable=False)
    language_id = Column(Integer, ForeignKey('languages.ID'), nullable=False)

    #country = relationship("Country", back_populates="secondary_languages")
    #language = relationship("Language", back_populates="secondary_languages")
