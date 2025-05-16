from fastapi import APIRouter
from .org import router as org_router
from .user import router as user_router
from .org import oauth2_org_scheme
from .user import oauth2_user_scheme

auth_router = APIRouter()

# Includi i router definiti nei file
auth_router.include_router(org_router, prefix="/org", tags=["Organizations"])
auth_router.include_router(user_router, prefix="/user", tags=["Users"])
