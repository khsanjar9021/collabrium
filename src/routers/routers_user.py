from fastapi import APIRouter, Depends, HTTPException,File, UploadFile, Query, Form, Request, Body, Path
from src.schemas.schemas_auth import CreateUserBase, UserBase, AccesTokenBase
from sqlalchemy.orm import Session
from src.models import User
from typing import List
from src.db import SessionLocal
from src.hashing import get_password_hash, verify_password
from typing import Union, Optional, Dict
from typing_extensions import Annotated
from src.token import create_access_token, get_current_user
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    tags=['Crud user']
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/api/user/get_all/", response_model=List[UserBase])
async def get_users(db: Session = Depends(get_db)):
    db_team = db.query(User).order_by(User.id.asc()).all()
    return db_team


@router.get("/api/user/get_one/", response_model=UserBase)
async def get_one_user(id:int, db:Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    db_one = db.query(User).filter_by(id=id).first()
    if not db_one:
        raise HTTPException(status_code=404, detail="Object does not  exist!!!")
    return db_one


@router.post("/api/user/create/", response_model=UserBase)
async def create_user(user: CreateUserBase = Body(...),
                             db: Session = Depends(get_db)):

    new_member = User(name=user.name, email=user.email, password=get_password_hash(user.password))
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member


@router.post("/token")
async def login_for_access_token(request:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    db_user = db.query(User).filter_by(email=request.username).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="Invalid email !!!")
    if not verify_password(request.password,db_user.password):
        raise HTTPException(status_code=404, detail="Invalid password !!!")
    access_token = create_access_token(data={"sub":request.username})
    return {"access_token": access_token, "token_type": "bearer"}