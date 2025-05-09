from pydantic import BaseModel
from typing import Optional, List
from .language import LanguageSchema
from .currency import CurrencySchema

class CountrySchema(BaseModel):
    ID: int
    name: str
    code: str
    description: Optional[str] = None
    language: LanguageSchema
    currency: CurrencySchema

    class Config:
        from_attributes = True

class CountryCreate(BaseModel):
    name: str
    code: str
    lang: int
    currency: int
    description: Optional[str] = None

class CountryImageSchema(BaseModel):
    id: int
    country_id: int
    url: str

    class Config:
        from_attributes = True

class CountryOnlyNameSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True