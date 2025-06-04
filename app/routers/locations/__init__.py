from fastapi import APIRouter
from .country import router as country_router
from .city import router as city_router
from .hotel import router as hotel_router
from .rooms import router as rooms_router

locations_router = APIRouter()

# Includi i router definiti nei file
locations_router.include_router(country_router, prefix="/countries", tags=["Countries"])
locations_router.include_router(city_router, prefix="/cities", tags=["Cities"])
locations_router.include_router(hotel_router, prefix="/hotels", tags=["Hotels"])
locations_router.include_router(rooms_router, prefix="/rooms", tags=["Rooms"])



@locations_router.get("/", summary="Locations API Root")


async def locations_root():
    return {"message": "Welcome to the Locations API. Use the endpoints to manage countries, cities, hotels, and rooms."}
