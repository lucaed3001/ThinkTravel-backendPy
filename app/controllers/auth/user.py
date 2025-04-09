from app.models import Country, User, UserImage
from sqlalchemy.orm import Session
from app.controllers.lib import get_password_hash, verify_password, create_access_token, get_user_images_data, get_image_file, get_profile_image_file
from app.schemas.user import UserCreate, UserSchema, UserLogin, UserImageSchema
from fastapi import HTTPException
from typing import List
from fastapi.responses import FileResponse

def login_user(db: Session, user_data: UserSchema):
    try:
        user = db.query(User).filter(User.email == user_data.email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        elif not verify_password(user_data.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid password")
        user.password = None  # Non restituire la password
        user.token = create_access_token(data={"sub": user.email})
        user.country = user.country
        return UserSchema.model_validate(user)
    except Exception as e:
        raise Exception(f"Error fetching users: {str(e)}")

def register_user(user_data: UserCreate, db: Session):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        password=hashed_password,
        name=user_data.name,
        surname=user_data.surname,
        country=user_data.country
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    new_user.password = None
    
    return UserSchema.model_validate(new_user)


def get_users(db: Session) -> List[UserSchema]:
    try:
        users = db.query(User).all()
        return [UserSchema.model_validate(user, from_attributes=True) for user in users]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching users: {str(e)}")
    
def get_images_user(db: Session, id: int) -> List[UserImageSchema]:
        return get_user_images_data(db, id, source=False)

def get_images_user_file(db: Session, id: int) -> FileResponse:
    images = get_user_images_data(db, id, source=True)
    url = images[0].url if images else None
    return get_image_file(url) if images else None

def get_profile_image(db: Session, id: int) -> FileResponse:
    return get_profile_image_file(id)


