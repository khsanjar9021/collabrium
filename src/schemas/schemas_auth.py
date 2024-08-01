from pydantic import BaseModel



class CreateUserBase(BaseModel):
    name: str
    email: str
    password: str


class UserBase(CreateUserBase):
    id: int

class AccesTokenBase(BaseModel):
    email: str
    password: str


    class Config:
        orm_mode = True