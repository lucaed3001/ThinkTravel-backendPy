from pydantic import BaseModel

class CurrencySchema(BaseModel):
    ID: int
    name: str
    simbol: str

    class Config:
        from_attributes = True
