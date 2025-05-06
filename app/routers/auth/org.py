from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models import User
from passlib.context import CryptContext
from app.controllers.auth.org import login_org, register_org, get_orgs
from app.schemas.org import OrgCreate, OrgLogin, OrgSchema  # Import userCreate schema
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.get("/all", summary="Get all orgs", response_model=list[OrgSchema])
async def get_users_endpoint(db: Session = Depends(get_db)):
    return get_orgs(db)


@router.post("/login", summary="Login org", response_model=OrgSchema)
async def login_org_form(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    org_login = OrgLogin(email=form_data.username, password=form_data.password)
    return login_org(db, org_data=org_login)


@router.post("/register", summary="Register org", response_model=OrgSchema)
async def register(org: OrgCreate, db: Session = Depends(get_db)):
    return register_org(org, db=db)