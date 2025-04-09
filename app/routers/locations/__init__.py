from fastapi import APIRouter
from .country import router as country_router

locations_router = APIRouter()

# Includi i router definiti nei file
locations_router.include_router(country_router, prefix="/countries", tags=["Countries"])
