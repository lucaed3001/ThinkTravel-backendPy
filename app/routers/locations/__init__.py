from fastapi import APIRouter
from .country import router as country_router
from .city import router as city_router

locations_router = APIRouter()

# Includi i router definiti nei file
locations_router.include_router(country_router, prefix="/countries", tags=["Countries"])
locations_router.include_router(city_router, prefix="/cities", tags=["cities"])
