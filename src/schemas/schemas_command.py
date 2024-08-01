import json
from datetime import datetime
from pydantic import BaseModel, model_validator
from typing import Union, List, Optional, Dict
from typing_extensions import Annotated


class NameBase(BaseModel):
    uz:str
    ru:str
    en:str
class UpdateTeamBase(BaseModel):
    name:NameBase
    position:NameBase
    description:NameBase

    @model_validator(mode="before")
    @classmethod
    def to_py_dict(cls, data):
        return json.loads(data)

class CreateMemberBase(BaseModel):
    name: NameBase
    position: NameBase
    description: NameBase

    @model_validator(mode="before")
    @classmethod

    def to_py_dict(cls, data):
        return json.loads(data)

class TeamBase(BaseModel):
    id:int
    name:NameBase
    image_url: Union[str, None]
    position: NameBase
    description: NameBase


    class Config:
        orm_mode = True