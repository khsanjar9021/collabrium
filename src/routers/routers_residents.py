import shutil
import os
from fastapi import APIRouter, Depends, HTTPException,File, UploadFile, Query, Form, Request, Body
from src.schemas.schemas_command import TeamBase, CreateMemberBase, UpdateTeamBase
from sqlalchemy.orm import Session
from src.models import Resident
from typing import List, Union
from src.db import SessionLocal
from typing_extensions import Annotated
from urllib.parse import urlparse

router = APIRouter(
    tags=['Crud residents']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/api/resident/get_all/",response_model=List[TeamBase])
async def get_resident(db: Session = Depends(get_db)):
    db_team = db.query(Resident).order_by(Resident.id.asc()).all()
    return db_team


@router.get("/api/resident/get_one/", response_model=TeamBase)
async def get_one_resident(id:int, db:Session = Depends(get_db)):
    db_one = db.query(Resident).filter_by(id=id).first()
    if not db_one:
        raise HTTPException(status_code=404, detail="Object does not  exist!!!")
    return db_one


@router.post("/api/resident/create/")
async def create_resident_member(request: Request,
                             file: UploadFile = File(None),
                            member: CreateMemberBase = Body(None),
                             db: Session = Depends(get_db)):
    img = {}
    req_url = request.base_url
    if file is not None:
        with open(f"static/tmp/resident/{file.filename}", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        image_url = f"{req_url}static/tmp/resident/{file.filename}"
        img["img"] = image_url
    new_member = Resident(image_url=img.get("img"), name=member.name.model_dump(),
                      position=member.position.model_dump(),
                      description=member.description.model_dump())
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member


@router.put("/api/resident/update/{id}", response_model=TeamBase)
async def update_resident_member(request:Request, id:int,
                            file: UploadFile = File(None),
                             member: UpdateTeamBase = Body(None),
                              db:Session = Depends(get_db)):
    db_id = db.query(Resident).filter_by(id=id).first()
    if not db_id:
        raise HTTPException(status_code=404, detail="Object was not found!!!")

    base_url = request.base_url
    db_id.name = member.name.model_dump()
    db_id.position = member.position.model_dump()
    db_id.description = member.description.model_dump()
    if db_id.image_url is not None and file is not None:
        parsed_url = urlparse(db_id.image_url)
        path = parsed_url.path.lstrip('/')
        os.unlink(path)
    if file is not None and file is not None:
        db_id.image_url = f"{base_url}static/tmp/resident/{file.filename}"
        with open(f"static/tmp/resident/{file.filename}", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    db.commit()
    return db_id


@router.delete("/api/resident/delete/{id}")
async def delete_resident_member(id:int, db:Session = Depends(get_db)):
    db_delete = db.query(Resident).filter_by(id=id)


    if not db_delete.first():
        raise HTTPException(status_code=404, detail="Object not found")
    parsed_url = urlparse(db_delete.first().image_url)
    path = parsed_url.path.lstrip('/')
    os.unlink(path)
    db_delete.delete()
    db.commit()
    return HTTPException(status_code=200, detail="Object has been deleted!!")


