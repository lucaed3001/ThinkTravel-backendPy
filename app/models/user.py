from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    country = Column(Integer, ForeignKey("countries.ID"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    country_rel = relationship("Country", back_populates="users")
    images = relationship('UserImage', back_populates='user', cascade='all, delete-orphan')

class UserImage(Base):
    __tablename__ = 'user_images'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    url = Column(String, nullable=False)
    
    user = relationship('User', back_populates='images')
