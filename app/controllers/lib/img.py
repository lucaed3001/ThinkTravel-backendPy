from app.models import Country, User, UserImage
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserSchema, UserLogin, UserImageSchema
from fastapi import HTTPException
from typing import List
from fastapi.responses import FileResponse
from pathlib import Path
import os

def get_user_images_data(db: Session, id: int, source: bool = False) -> List[UserImageSchema]:
    try:
        images = db.query(UserImage).filter(UserImage.user_id == id).all()
        if not images:
            raise HTTPException(status_code=404, detail="User images not found")
        if source:
            return [UserImageSchema.model_validate(img, from_attributes=True) for img in images]
        else:
            return [
                {"id": img.id, "user_id": img.user_id}  # Exclude the `url` field
                for img in images
            ]
    except Exception as e:
        if(isinstance(e, HTTPException)):
            raise e
        else:
            raise HTTPException(status_code=500, detail=f"Error fetching user images: {str(e)}")
        
def get_image_file(source) -> FileResponse:
    try:
        if source:
            base_dir = os.getcwd()
            image_path = Path(source) 
            print(base_dir)
            if not image_path.exists():
                raise HTTPException(status_code=404, detail="Image not found")
            return FileResponse(source, media_type="image/jpeg")
        else:
            raise HTTPException(status_code=400, detail="No image source provided")
    except Exception as e:
        if(isinstance(e, HTTPException)):
            raise e
        else:
            raise HTTPException(status_code=500, detail=f"Error fetching image: {str(e)}")
        
def get_profile_image_file(id) -> FileResponse:
    try:
        base_dir = os.getcwd()
        image_path = Path(base_dir) / "app" / "static" / "images" / "profile" / f"{id}.jpg"
        if not image_path.exists(): 
            image_path = Path(base_dir) / "app" / "static" / "images" / "profile" / f"{id}.png"
            if not image_path.exists(): 
                image_path = Path(base_dir) / "app" / "static" / "images" / "profile" / f"{id}.jpeg"
                if not image_path.exists(): 
                    image_path = Path(base_dir) / "app" / "static" / "images" / "profile" / f"{id}.gif"
                    if not image_path.exists(): 
                        image_path = Path(base_dir) / "app" / "static" / "images" / "profile" / "default.jpg"


        return FileResponse(
            path=image_path,
            media_type="image/jpeg",
            headers={"Content-Disposition": "inline"}
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching image: {str(e)}")