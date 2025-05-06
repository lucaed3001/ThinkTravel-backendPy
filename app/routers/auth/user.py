from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models import User
from pathlib import Path
import shutil
from passlib.context import CryptContext
from app.controllers.auth import login_user, register_user, get_users, get_images_user, get_images_user_file, get_profile_image, put_profile_image
import app.controllers.lib as lib
from app.schemas.user import UserCreate, UserSchema, UserLogin  # Import userCreate schema
from fastapi.responses import FileResponse
import os
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/user/login")
router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.get("/all", summary="Get all users", response_model=list[UserSchema])
async def get_users_endpoint(db: Session = Depends(get_db)):
    return get_users(db)

@router.post("/login", summary="Login user")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_login = UserLogin(email=form_data.username, password=form_data.password)
    return login_user(db, user_data=user_login)

"""@router.post("/login", response_model=UserSchema, summary="Login user")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    return login_user(db, user_data=user)"""


@router.post("/register", response_model=UserSchema, summary="Register user")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    return register_user(user, db=db)

@router.get("/token", summary="Get token user")
async def get_token_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(status_code=400, detail="Token is missing")
    return {"token": token}

@router.get("/image", summary="Get image of a user", )
async def get_user_image_f(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    id = lib.verify_token(token)
    id = id.get("id")
    if id is None:
        raise HTTPException(status_code=400, detail="Invalid token")
    return get_profile_image(db, id=id)

@router.post("/upload-image/")
async def upload_image(file: UploadFile = File(...), db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    id = lib.verify_token(token)
    id = id.get("id")
    if id is None:
        raise HTTPException(status_code=400, detail="Invalid token")
    return put_profile_image(db, file=file, id=id)

@router.get("/me", summary="Get user data")
async def get_user_data(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    id = lib.verify_token(token)
    id = id.get("id")
    if id is None:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserSchema.model_validate(user, from_attributes=True)
