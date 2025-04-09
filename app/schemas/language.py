from pydantic import BaseModel

class LanguageSchema(BaseModel):
    ID: int
    name: str
    code: str

    class Config:
        from_attributes = True
