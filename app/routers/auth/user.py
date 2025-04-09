from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models import User
from pathlib import Path
import shutil
from passlib.context import CryptContext
from app.controllers.auth import login_user, register_user, get_users, get_images_user, get_images_user_file, get_profile_image
from app.schemas.user import UserCreate, UserSchema, UserLogin, UserImageSchema  # Import userCreate schema
from fastapi.responses import FileResponse
import os

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.get("/all", summary="Get all users", response_model=list[UserSchema])
async def get_users_endpoint(db: Session = Depends(get_db)):
    return get_users(db)


@router.post("/login", response_model=UserSchema, summary="Login user")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    return login_user(db, user_data=user)


@router.post("/register", response_model=UserSchema, summary="Register user")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    return register_user(user, db=db)


@router.get("/image/{id}", summary="Get image of a user")
async def get_user_image_f(id: int, db: Session = Depends(get_db)):
    return get_profile_image(db, id=id)

@router.post("/upload-image/")
async def upload_image(file: UploadFile = File(...), id: int = 0, db: Session = Depends(get_db)):
    try:
        save_dir = Path("app/static/images/profile")
        save_dir.mkdir(parents=True, exist_ok=True)

        original_extension = os.path.splitext(file.filename)[1]
        if original_extension.lower() not in [".jpg", ".jpeg", ".png", ".gif"]:
            raise HTTPException(status_code=400, detail="Formato file non supportato")

        file_path = save_dir / f"{id}{original_extension.lower()}"

        for ext in [".jpg", ".jpeg", ".png", ".gif"]:
            old_file = save_dir / f"{id}{ext}"
            if old_file.exists():
                old_file.unlink()

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {"filename": file_path.name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
