from app.models import Country, Organizator as org
from sqlalchemy.orm import Session
from app.controllers.lib import get_password_hash, verify_password, create_access_token
from app.schemas.org import OrgCreate, OrgSchema, OrgLogin
from fastapi import HTTPException
from typing import List

"""def login_org(db: Session, org_data: OrgSchema):
    try:
        org_r = db.query(org).filter(org.email == org_data.email).first()
        if not org_r:
            raise HTTPException(status_code=404, detail="org not found")
        elif not verify_password(org_data.password, org_r.password):
            raise HTTPException(status_code=401, detail="Invalid password")
        org_r.password = None  # Non restituire la password
        org_r.token = create_access_token(data={"sub": org_r.email, "org_id": org_r.id})

        return OrgSchema.model_validate(org_r)
    except Exception as e:
        raise Exception(f"Error fetching orgs: {str(e)}")
        """

def login_org(db: Session, org_data: OrgSchema):
    try:
        user = db.query(org).filter(org.email == org_data.email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        elif not verify_password(org_data.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid password")
        user.password = None 
        token = create_access_token(
            data={
                "sub": user.email,
                "id": user.id,
                "name": user.name
            })
        return {"access_token": token,"token_type": "bearer"}
    
    except Exception as e:
        raise Exception(f"Error fetching users: {str(e)}")

def register_org(org_data: OrgCreate, db: Session):
    existing_org = db.query(org).filter(org.email == org_data.email).first()
    if existing_org:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(org_data.password)
    new_org = org(
        name=org_data.name,
        address=org_data.address,
        city=org_data.city,
        phone=org_data.phone,
        email=org_data.email,
        password=hashed_password,
        vat=org_data.vat
    )

    db.add(new_org)
    db.commit()
    db.refresh(new_org)
    new_org.password = None
    
    return OrgSchema.model_validate(new_org)


def get_orgs(db: Session) -> List[OrgSchema]:
    try:
        orgs = db.query(org).all()
        return [OrgSchema.model_validate(org, from_attributes=True) for org in orgs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching orgs: {str(e)}")
    
def get_org_by_id(db: Session, id: int) -> OrgSchema:
    try:
        organizator = db.query(org).filter(org.id == id).first()
        
        if not organizator:
            raise HTTPException(status_code=404, detail="Org not found")
        
        return OrgSchema.model_validate(organizator, from_attributes=True)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching org by ID: {str(e)}")
