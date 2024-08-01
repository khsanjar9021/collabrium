import shutil
import os
from fastapi import APIRouter, Depends, HTTPException,File, UploadFile, Query, Form, Request, Body
from src.schemas.schemas_faq import FaqBase, CreateFaqBase
from sqlalchemy.orm import Session
from src.models import FAQ, Space
from typing import List, Optional, Union, Text
from src.db import SessionLocal
from typing_extensions import Annotated

router = APIRouter(
    tags=['Crud FAQ']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/api/faq/get_all/", response_model=Union[List[FaqBase], FaqBase])
async def get_one_all_faq(id:int = Query(None), db:Session = Depends(get_db)):
    db_id = db.query(FAQ).filter_by(id=id).first()
    if id is None:
        db_one_all = db.query(FAQ).order_by(FAQ.id.asc()).all()
        return db_one_all
    if db_id:
        db_one_id = db.query(FAQ).filter_by(id=id).first()
        return db_one_id
    else:
        raise HTTPException(status_code=404, detail="Object was not found!!!")

@router.get("/api/faq/get_space/{space_id}/", response_model=List[FaqBase])
async def get_space(space_id:int,db:Session = Depends(get_db)):
    db_space = db.query(FAQ).filter_by(space_id=space_id).all()
    if not db_space:
        raise HTTPException(status_code=404, detail="Object was not found!!!")
    return db_space

@router.post("/api/faq/create/")
async def create_faq(faq: CreateFaqBase = Body(None),db: Session = Depends(get_db)):
    db_space = db.query(Space).filter_by(id=faq.space_id).first()
    if not db_space:
        raise HTTPException(status_code=404, detail="Space_id  does not exist!!!")
    new_member = FAQ(question=faq.question.model_dump(), answer=faq.answer.model_dump(), space_id=faq.space_id)
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member


@router.put("/api/faq/update/{id}/")
async def update_faq(id:int,faq: CreateFaqBase = Body(None), db:Session = Depends(get_db)):
    db_id = db.query(FAQ).filter_by(id=id).first()
    db_space = db.query(Space).filter_by(id=faq.space_id).first()
    if not db_id:
        raise HTTPException(status_code=404, detail="Object was not found!!!")
    if not db_space:
        raise HTTPException(status_code=404, detail="Space_id was not found!!!")
    db_id.space_id = faq.space_id
    db_id.question = faq.question.model_dump()
    db_id.answer = faq.answer.model_dump()
    db.commit()
    raise HTTPException(status_code=201, detail="Object has been updated successfully!!!")



@router.delete("/api/faq/delete/{id}/")
async def delete_faq(id:int, db:Session = Depends(get_db)):
    db_delete = db.query(FAQ).filter_by(id=id)

    if not db_delete.first():
        raise HTTPException(status_code=404, detail="Object not found")
    db_delete.delete()
    db.commit()
    return HTTPException(status_code=200, detail="Object has been deleted!!")
