import shutil
import os
from fastapi import APIRouter, Depends, HTTPException,File, UploadFile, Query, Form, Request, Body
from src.schemas.schemas_cards_blog import CardsBase, CreateCardsBase
from sqlalchemy.orm import Session
from src.models import Cards_blog
from typing import List, Union
from src.db import SessionLocal
from typing_extensions import Annotated
from urllib.parse import urlparse

router = APIRouter(
    tags=['Crud Cards_blog']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/api/cards_blog/get_all/")
async def get_cards_blog(db: Session = Depends(get_db)):
    db_team = db.query(Cards_blog).order_by(Cards_blog.id.asc()).all()
    return db_team


@router.get("/api/cards_blog/get_one/")
async def get_one_cards_blog(id:int, db:Session = Depends(get_db)):
    db_one = db.query(Cards_blog).filter_by(id=id).first()
    if not db_one:
        raise HTTPException(status_code=404, detail="Object does not  exist!!!")
    return db_one


@router.post("/api/cards_blog/create/")
async def create_resident_member(request: Request,
                             file: UploadFile = File(None),
                            cards_blog: CreateCardsBase = Body(None),
                             db: Session = Depends(get_db)):
    img = {}
    req_url = request.base_url
    if file is not None:
        with open(f"static/tmp/cards_blog/{file.filename}", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        image_url = f"{req_url}static/tmp/cards_blog/{file.filename}"
        img["img"] = image_url
    new_member = Cards_blog(image=img.get("img"), title=cards_blog.title.model_dump(),
                      url=cards_blog.url,created_at=cards_blog.created_at)
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member


@router.put("/api/cards_blogt/update/{id}", response_model=CardsBase)
async def update_crards_blog(request:Request, id:int,
                            file: UploadFile = File(None),
                             cards_blog: CreateCardsBase = Body(None),
                              db:Session = Depends(get_db)):
    db_id = db.query(Cards_blog).filter_by(id=id).first()
    if not db_id:
        raise HTTPException(status_code=404, detail="Object was not found!!!")

    base_url = request.base_url
    db_id.url = cards_blog.url
    db_id.title = cards_blog.title.model_dump()
    db_id.created_at = cards_blog.created_at

    if db_id.image is not None and file is not None:
        parsed_url = urlparse(db_id.image)
        path = parsed_url.path.lstrip('/')
        os.unlink(path)
    if file is not None and file is not None:
        db_id.image = f"{base_url}static/tmp/cards_blog/{file.filename}"
        with open(f"static/tmp/cards_blog/{file.filename}", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    db.commit()
    return db_id


@router.delete("/api/cards_blog/delete/{id}")
async def delete_cards_blog(id:int, db:Session = Depends(get_db)):
    db_delete = db.query(Cards_blog).filter_by(id=id)
    if not db_delete.first():
        raise HTTPException(status_code=404, detail="Object was not found")
    parsed_url = urlparse(db_delete.first().image)
    path = parsed_url.path.lstrip('/')
    os.unlink(path)
    db_delete.delete()
    db.commit()
    return HTTPException(status_code=200, detail="Object has been deleted!!")


