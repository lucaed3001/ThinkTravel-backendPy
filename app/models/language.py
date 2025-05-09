from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Language(Base):
    __tablename__ = "languages"

    ID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(30), unique=True, nullable=False)
    code = Column(String(2), nullable=False)

#secondary_languages = relationship("SecondaryLanguage", back_populates="language")