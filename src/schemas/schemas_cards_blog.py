import json
from datetime import datetime
from pydantic import BaseModel, model_validator
from typing import Union, List, Optional, Dict
from typing_extensions import Annotated


class NameBase(BaseModel):
    uz:str
    ru:str
    en:str

class CreateCardsBase(BaseModel):
    created_at: datetime
    image: str
    title: NameBase
    url: str

    @model_validator(mode="before")
    @classmethod
    def to_py_dict(cls, data):
        return json.loads(data)


class CardsBase(BaseModel):
    id:int
    created_at: datetime
    image: Union[str, None]
    title: NameBase
    url: str


    class Config:
        orm_mode = True