import json
from datetime import datetime
from pydantic import BaseModel, model_validator
from typing import Union, List, Optional, Dict
from typing_extensions import Annotated


class NameBase(BaseModel):
    uz:str
    ru:str
    en:str

class CreateFaqBase(BaseModel):
    space_id: int
    question: NameBase
    answer: NameBase

class FaqBase(CreateFaqBase):
    id: int



    class Config:
        orm_mode = True