from pydantic import BaseModel
from typing import Optional
from app.schemas.city import CitySchema  # o CityOnlyNameSchema, se preferisci solo il nome
from app.schemas.org import OrgSchema  # crea uno schema anche per questo

class HotelSchema(BaseModel):
    id: int
    name: str
    address: str
    city: int
    description: Optional[str]
    graduation: Optional[int]
    organizer: int 
    star_number: int

    class Config:
        from_attributes = True
    

class HotelCreate(BaseModel):
    name: Optional[str]
    address: Optional[str]
    city: Optional[int]
    description: Optional[str]
    organizer: Optional[int]
    star_number: Optional[int]

class HotelFullSchema(BaseModel):
    id: int
    name: str
    address: str
    city: Optional[CitySchema]
    description: Optional[str]
    graduation: Optional[int]
    organizer: Optional[OrgSchema]
    star_number: int

    class Config:
        from_attributes = True
