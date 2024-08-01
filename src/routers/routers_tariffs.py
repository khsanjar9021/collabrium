import shutil
import os
from fastapi import APIRouter, Depends, HTTPException,File, UploadFile, Query, Form, Body
from src.schemas.schemas_tariff import CreateTariffBase, TariffBase
from sqlalchemy.orm import Session
from src.models import Tariff
from typing import List, Optional
from src.db import SessionLocal
from typing_extensions import Annotated

router = APIRouter(
    tags=['Crud tariffs']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/api/tariffs/get_all/",response_model=List[TariffBase])
async def get_tariff(db: Session = Depends(get_db)):
    db_team = db.query(Tariff).order_by(Tariff.id.asc()).all()
    return db_team


@router.get("/api/tariff/get_one/{id}/")
async def get_one_tariff(id:int, db:Session = Depends(get_db)):
    db_one = db.query(Tariff).filter_by(id=id).first()
    if not db_one:
        raise HTTPException(status_code=404, detail="Object does not  exist!!!")

    return db_one

@router.post("/api/tariff/create/")
async def create_tariff(tariff: CreateTariffBase = Body(None), db: Session = Depends(get_db)):
    new_tariff = Tariff(space_id = tariff.space_id,
                        to = tariff.to, tabs = tariff.tabs,
                        service = tariff.service)

    db.add(new_tariff)
    db.commit()
    db.refresh(new_tariff)
    return new_tariff


@router.put("/api/tariff/update/{id}/")
async def update_tariff(id: int, tariff: CreateTariffBase = Body(None), db: Session = Depends(get_db)):
    db_upd = db.query(Tariff).filter_by(id=id).first()
    if not db_upd:
        raise HTTPException(status_code=404, detail="Updating object was not found")
    db_upd.to = tariff.to
    db_upd.tabs = tariff.tabs
    db_upd.service = tariff.service
    db_upd.space_id = tariff.space_id
    db.commit()
    raise HTTPException(status_code=201, detail="Object has been updated successfully!!!")


@router.delete("/api/tariff/delete/{id}/")
async def delete_team_member(id:int, db:Session = Depends(get_db)):
    db_delete = db.query(Tariff).filter_by(id=id)

    if not db_delete.first():
        raise HTTPException(status_code=404, detail="Deleting object was not found")
    db_delete.delete()
    db.commit()
    return HTTPException(status_code=200, detail="Object has been deleted!!")


