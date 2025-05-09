from pydantic import BaseModel
from typing import Optional
from app.schemas.country import CountryOnlyNameSchema

class CitySchema(BaseModel):
    id: int
    name: str
    country: CountryOnlyNameSchema
    description: Optional[str] = None

    class Config:
        from_attributes = True

class CityCreate(BaseModel):
    name: str
    country: int
    description: Optional[str] = None

class CityImageSchema(BaseModel):
    id: int
    city_id: int
    url: str

    class Config:
        from_attributes = True