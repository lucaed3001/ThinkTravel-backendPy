from pydantic import BaseModel

class SecondaryLanguageSchema(BaseModel):
    id: int
    country_id: int
    language_id: int

    class Config:
        from_attributes = True
