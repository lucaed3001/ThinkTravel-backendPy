from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models import User
from passlib.context import CryptContext
from app.controllers.auth.org import login_org, register_org, get_orgs
from app.schemas.org import OrgCreate, OrgLogin, OrgSchema  # Import userCreate schema

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.get("/all", summary="Get all orgs", response_model=list[OrgSchema])
async def get_users_endpoint(db: Session = Depends(get_db)):
    return get_orgs(db)


@router.post("/login", summary="Login org", response_model=OrgSchema)
async def login(org: OrgLogin, db: Session = Depends(get_db)):
    return login_org(db, org_data=org)


@router.post("/register", summary="Register org", response_model=OrgSchema)
async def register(org: OrgCreate, db: Session = Depends(get_db)):
    return register_org(org, db=db)