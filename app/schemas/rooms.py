from pydantic import BaseModel
from typing import Optional

class RoomBase(BaseModel):
    id: Optional[int] = None
    type: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    currency: Optional[int] = None
    idHotel: Optional[int] = None
    guest: Optional[int] = None
    tv: Optional[bool] = None
    balcony: Optional[bool] = None
    ac: Optional[bool] = None
    size: Optional[int] = None
    quantity: int

    class Config:
        from_attributes = True

class RoomTranslation(BaseModel):
    id: Optional[int] = None
    room_id: int
    lang: str
    description: Optional[str] = None

    class Config:
        from_attributes = True