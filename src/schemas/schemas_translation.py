import json
from datetime import datetime
from pydantic import BaseModel, model_validator
from typing import Union, List, Optional, Dict
from typing_extensions import Annotated


class NameBase(BaseModel):
    uz: str
    ru: str
    en: str

class UpdateTranslationBase(BaseModel):
    text: NameBase

    @model_validator(mode="before")
    @classmethod
    def to_py_dict(cls, data):
        return json.loads(data)

class CreateTranslationBase(BaseModel):
    text: NameBase

    @model_validator(mode="before")
    @classmethod

    def to_py_dict(cls, data):
        return json.loads(data)

class TranslationBase(BaseModel):
    id:int
    text:NameBase
    image: Union[str, None]


    class Config:
        orm_mode = True