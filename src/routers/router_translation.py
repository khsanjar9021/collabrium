import json
import os
import shutil
from fastapi import APIRouter, Depends, HTTPException,File, UploadFile, Query, Form, Request, Body, Path
from src.schemas.schemas_translation import TranslationBase, CreateTranslationBase, UpdateTranslationBase
from sqlalchemy.orm import Session
from src.models import Translation
from typing import List
from src.db import SessionLocal
from typing import Union, Optional, Dict
from typing_extensions import Annotated
from urllib.parse import urlparse
from src.translation import name


router = APIRouter(
    tags=['Crud translation']
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/api/translation/get_all/", response_model=List[TranslationBase])
async def get_translation(db: Session = Depends(get_db)):
    db_team = db.query(Translation).order_by(Translation.id.asc()).all()
    return db_team


@router.get("/api/translation/get_one/", response_model=TranslationBase)
async def get_one_translation(id:int, db:Session = Depends(get_db)):
    db_one = db.query(Translation).filter_by(id=id).first()
    if not db_one:
        raise HTTPException(status_code=404, detail="Object does not  exist!!!")
    return db_one


@router.post("/api/translation/create/", response_model=TranslationBase)
async def create_translation(request: Request,
                             file: UploadFile = File(None),
                             text: CreateTranslationBase = Body(None),
                             db: Session = Depends(get_db)):
    image = {}
    req_url = request.base_url
    if file is not None:
        with open(f"static/tmp/translation/{file.filename}", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        image_url = f"{req_url}static/tmp/translation/{file.filename}"
        image["img"] = image_url
    new_member = Translation(image=image.get("img"), text=text.text.model_dump())
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member


@router.put("/api/translation/update/{id}/", response_model=TranslationBase)
async def update_translation(request:Request, id:int,
                            file: UploadFile = File(None),
                            text: CreateTranslationBase = Body(None),
                              db:Session = Depends(get_db)):
    db_id = db.query(Translation).filter_by(id=id).first()
    if not db_id:
        raise HTTPException(status_code=404, detail="Object was not found!!!")
    base_url = request.base_url
    db_id.text = text.text.model_dump()

    if db_id.image is not None and file is not None:
        parsed_url = urlparse(db_id.image)
        path = parsed_url.path.lstrip('/')
        os.unlink(path)
    if file is not None:
        db_id.image = f"{base_url}static/tmp/translation/{file.filename}"
        with open(f"static/tmp/translation/{file.filename}", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    db.commit()
    return db_id

@router.delete("/api/translation/delete/{id}")
async def delete_translation(id:int, db:Session = Depends(get_db)):
    db_delete = db.query(Translation).filter_by(id=id)
    if not db_delete.first():
        raise HTTPException(status_code=404, detail="Object was not found")
    if db_delete.first().image is not None:
        parsed_url = urlparse(db_delete.first().image)
        path = parsed_url.path.lstrip('/')
        os.unlink(path)
    db_delete.delete()
    db.commit()
    return HTTPException(status_code=200, detail="Object has been deleted!!")
