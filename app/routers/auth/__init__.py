from fastapi import APIRouter
from .org import router as org_router
from .user import router as user_router

auth_router = APIRouter()

# Includi i router definiti nei file
auth_router.include_router(org_router, prefix="/org", tags=["Organizations"])
auth_router.include_router(user_router, prefix="/user", tags=["Users"])
