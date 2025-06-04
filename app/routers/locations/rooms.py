from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import RoomBase
from app.controllers.locations import get_all_rooms

router = APIRouter()

"""@router.post("/", response_model=RoomResponse)
def create_new_room(room: RoomCreate, db: Session = Depends(get_db)):
    db_room = create_room(db, room)
    if not db_room:
        raise HTTPException(status_code=400, detail="Room could not be created")
    return db_room

@router.get("/{room_id}", response_model=RoomResponse)
def read_room(room_id: int, db: Session = Depends(get_db)):
    db_room = get_room_by_id(db, room_id)
    if not db_room:
        raise HTTPException(status_code=404, detail="Room not found")
    return db_room"""

@router.get("/", response_model=list[RoomBase])
def read_all_rooms(db: Session = Depends(get_db), ):
    return get_all_rooms(db)