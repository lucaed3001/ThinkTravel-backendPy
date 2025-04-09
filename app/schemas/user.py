from pydantic import BaseModel, EmailStr
from typing import Optional, Union

class UserSchema(BaseModel):
    id: int
    email: EmailStr
    name: str
    surname: str
    country: int
    token: Optional[str] = None

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    surname: str
    country: int

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserImageSchema(BaseModel):
    id: int
    user_id: int
    url: Optional[str] = None

    class Config:
        from_attributes = True