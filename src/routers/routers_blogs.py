import shutil
import os
from fastapi import APIRouter, Depends, HTTPException,File, UploadFile, Query, Form, Body, Request
from src.schemas.schemas_blog import CreateBlogBase, BlogBase
from sqlalchemy.orm import Session
from src.models import Blog
from typing import List, Union, Optional, NewType, Any, Callable
from src.db import SessionLocal
from typing_extensions import Annotated
from urllib.parse import urlparse
router = APIRouter(
    tags=['Crud blog']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.get("/api/blog/get_all/",response_model=List[BlogBase])
async def get_all_blogs(db: Session = Depends(get_db)):
    db_team = db.query(Blog).order_by(Blog.id.asc()).all()
    return db_team


@router.get("/api/blog/get_one/{id}/", response_model=BlogBase)
async def get_one_blog(id:int, db:Session = Depends(get_db)):
    db_one = db.query(Blog).filter_by(id=id).first()
    if not db_one:
        raise HTTPException(status_code=404, detail="Object does not  exist!!!")
    return db_one


@router.post("/api/create/blog/",response_model=BlogBase)
async def create_blog(request: Request, image_1: UploadFile = File(None),
                             image_2: UploadFile = File(None),
                             blog: CreateBlogBase = Body(None),
                             db: Session = Depends(get_db)):
    imgs = {}
    req_url = request.base_url
    if image_1 is not None:
        img_1 = f"{req_url}static/tmp/blog/{image_1.filename}"
        with open(f"static/tmp/blog/{image_1.filename}", "wb") as buffer:
            shutil.copyfileobj(image_1.file, buffer)
        imgs["img_1"] = img_1
    if image_2 is not None:
        img_2 = f"{req_url}static/tmp/blog/{image_2.filename}"
        with open(f"static/tmp/blog/{image_2.filename}", "wb") as buffer:
            shutil.copyfileobj(image_2.file, buffer)
        imgs["img_2"] = img_2
    blog = Blog(title=blog.title.model_dump(), blog_url=blog.blog_url,
                sub_title=blog.sub_title.model_dump(), image_1=imgs.get("img_1"),
                image_2= imgs.get("img_2"), body_1=blog.body_1.model_dump(), body_2=blog.body_2.model_dump())

    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog

@router.put("/api/blog/update/{id}/",response_model=BlogBase)
async def update_blog(request:Request, id:int,
                             image_1: UploadFile = File(None),
                             image_2: UploadFile = File(None),
                             blog: CreateBlogBase = Body(None),
                                 db:Session = Depends(get_db)):
    db_upd = db.query(Blog).filter_by(id=id).first()
    img = {}
    img["img_1"]=db_upd.image_1
    img["img_2"] = db_upd.image_2
    route = 'static/tmp/blog/'
    base_url = request.base_url
    if not db_upd:
        raise HTTPException(status_code=404, detail="Object not found")
    if db_upd.image_1 is not None and image_1 is not None:
        parsed_url = urlparse(img.get("img_1"))
        path = parsed_url.path.lstrip('/')
        os.unlink(path)
    if image_1 is not None:
        db_upd.image_1 = f"{base_url}{route}{image_1.filename}"
        with open(f"{route}{image_1.filename}", "wb") as buffer:
            shutil.copyfileobj(image_1.file, buffer)
    if db_upd.image_2 is not None and image_2 is not None:
        parsed_url = urlparse(img.get("img_2"))
        path = parsed_url.path.lstrip('/')
        os.unlink(path)
    if image_2 is not None:
        db_upd.image_2 = f"{base_url}{route}{image_2.filename}"
        with open(f"{route}{image_2.filename}", "wb") as buffer:
            shutil.copyfileobj(image_2.file, buffer)

    db_upd.blog_url = blog.blog_url
    db_upd.title = blog.title.model_dump()
    db_upd.sub_title = blog.sub_title.model_dump()
    db_upd.body_1 = blog.body_1.model_dump()
    db_upd.body_2 = blog.body_2.model_dump()
    db.commit()
    return db_upd


@router.delete("/api/blog/delete/{id}/")
async def delete_article(id:int, db:Session = Depends(get_db)):
    db_delete = db.query(Blog).filter_by(id=id)

    if not db_delete.first():
        raise HTTPException(status_code=404, detail="Object not found")
    if db_delete.first().image_1:
        parsed_url = urlparse(db_delete.first().image_1)
        path = parsed_url.path.lstrip('/')
        os.unlink(path)
    if db_delete.first().image_2:
        parsed_url = urlparse(db_delete.first().image_2)
        path = parsed_url.path.lstrip('/')
        os.unlink(path)
    db_delete.delete()
    db.commit()
    return HTTPException(status_code=200, detail="Object has been deleted!!")
