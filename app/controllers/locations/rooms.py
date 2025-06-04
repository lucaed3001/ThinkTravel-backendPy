from sqlalchemy.orm import Session, joinedload
from app.models.rooms import Room, RoomTranslation
from app.schemas import RoomBase
from typing import List

def get_all_rooms(db: Session, lang: str = "IT") -> List[RoomBase]:
    try:
        rooms = db.query(Room).options(
            joinedload(Room.translations)
        ).all()

        room_list = []

        for room in rooms:
            translation = next((t for t in room.translations if t.lang == lang), None)

            room_list.append({
                'id': room.id,
                'type': room.type,
                'name': room.name,
                'description': translation.description if translation and translation.description else room.description,
                'price': float(room.price) if room.price is not None else None,
                'currency': room.currency,
                'idHotel': room.idHotel,
                'guest': room.guest,
                'tv': bool(room.tv) if room.tv is not None else False,
                'balcony': bool(room.balcony) if room.balcony is not None else False,
                'ac': bool(room.ac) if room.ac is not None else False,
                'size': room.size,
                'quantity': room.quantity
            })

        return room_list

    except Exception as e:
        import traceback
        print("Errore durante il recupero delle stanze:", e)
        traceback.print_exc()
        return []

