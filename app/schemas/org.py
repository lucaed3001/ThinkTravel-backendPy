from pydantic import BaseModel, EmailStr
from typing import Optional

class OrgSchema(BaseModel):
    id: int
    name: str
    address: str
    city: int
    phone: str
    email: EmailStr
    vat: str
    token: Optional[str] = None

    class Config:
        from_attributes = True

class OrgCreate(BaseModel):
    name: str
    address: str
    city: int
    phone: str
    email: EmailStr
    password: str
    vat: str

class OrgLogin(BaseModel):
    email: EmailStr
    password: str
