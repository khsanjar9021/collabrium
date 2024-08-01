import json
from datetime import datetime
from pydantic import BaseModel, model_validator
from typing import Union, List, Optional, Dict
from typing_extensions import Annotated


class NameBase(BaseModel):
    uz:str
    ru:str
    en:str

class SpaceBase(BaseModel):
    id: int
    title: NameBase
    image: Union[str, None]

class CreateSpaceBase(BaseModel):
    title: NameBase

    @model_validator(mode="before")
    @classmethod
    def to_py_dict(cls, data):
        return json.loads(data)

    class Config:
        orm_mode = True