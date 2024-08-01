import json
from pydantic import BaseModel, model_validator, Json
from typing import Union, List, Optional, Dict
from typing_extensions import Annotated


class NameBase(BaseModel):
    uz: str
    ru: str
    en: str

class CreateBlogBase(BaseModel):
    title: NameBase
    blog_url: str
    sub_title: NameBase
    body_1: NameBase
    body_2: NameBase

    @model_validator(mode="before")
    @classmethod
    def to_py_dict(cls, data):
        return json.loads(data)


class BlogBase(BaseModel):
    id: int
    image_1: Union[str, None]
    image_2: Union[str, None]
    title: NameBase
    blog_url: str
    sub_title: NameBase
    body_1: NameBase
    body_2: NameBase


    class Config:
        orm_mode = True