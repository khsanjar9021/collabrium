import shutil
import os
from urllib.parse import urlparse
from fastapi import APIRouter, Depends, HTTPException,File, UploadFile, Query, Form,Request, Body
from src.schemas.schemas_space import SpaceBase, CreateSpaceBase
from src.schemas.schemas_auth import UserBase
from src.token import get_current_user
from sqlalchemy.orm import Session
from src.models import Space
from typing import List, Optional, Union
from src.db import SessionLocal
from typing_extensions import Annotated

router = APIRouter(
    tags=['Crud spaces']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/api/space/get_all/", response_model=List[SpaceBase])
async def get_space(db: Session = Depends(get_db)):
    db_team = db.query(Space).order_by(Space.id.asc()).all()
    return db_team


@router.get("/api/space/get_one/", response_model=SpaceBase)
async def get_one_space(id:int, db:Session = Depends(get_db),current_user: UserBase = Depends(get_current_user)):
    db_one = db.query(Space).filter_by(id=id).first()
    if not db_one:
        raise HTTPException(status_code=404, detail="Object does not  exist!!!")
    return db_one


@router.post("/api/space/create/", response_model=SpaceBase)
async def create_space(request: Request,
                             file: UploadFile = File(None),
                             space: CreateSpaceBase = Body(None),
                             db: Session = Depends(get_db)):
    img = {}
    req_url = request.base_url
    if file is not None:
        with open(f"static/tmp/spaces/{file.filename}", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        image_url = f"{req_url}static/tmp/spaces/{file.filename}"
        img["img"] = image_url
    new_member = Space(image = img.get("img"), title = space.title.model_dump())
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member

@router.put("/api/space/update/{id}", response_model=SpaceBase)
async def update_space(request:Request, id:int,
                            file: UploadFile = File(None),
                             space: CreateSpaceBase = Body(None),
                              db:Session = Depends(get_db)):
    db_id = db.query(Space).filter_by(id=id).first()
    if not db_id:
        raise HTTPException(status_code=404, detail="Object was not found!!!")
    base_url = request.base_url
    if db_id.image is not None and file is not None:
        parsed_url = urlparse(db_id.image)
        path = parsed_url.path.lstrip('/')
        os.unlink(path)
    if file is not None:
        db_id.image = f"{base_url}static/tmp/spaces/{file.filename}"
        with open(f"static/tmp/spaces/{file.filename}", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    db_id.title = space.title.model_dump()
    db.commit()
    return db_id


@router.delete("/api/spaces/delete/{id}")
async def delete_space(id:int, db:Session = Depends(get_db)):
    db_delete = db.query(Space).filter_by(id=id)

    if not db_delete.first():
        raise HTTPException(status_code=404, detail="Object not found")
    if db_delete.first().image is not None:
        parsed_url = urlparse(db_delete.first().image)
        path = parsed_url.path.lstrip('/')
        os.unlink(path)
    db_delete.delete()
    db.commit()
    return HTTPException(status_code=200, detail="Object has been deleted!!")


