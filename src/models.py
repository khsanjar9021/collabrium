from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,Text,ARRAY, DateTime, func, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import ImageType
from src.db import Base



# metadata = MetaData()
#
# team = Table(
#     "team",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("image_url", String, index=True),
#     Column("name", String, index=True),
#     Column("position", String, index=True),
#     Column("description", String, index=True),

class Team(Base):

    __tablename__= "team"

    id = Column(Integer, primary_key=True)
    image_url = Column(String, index=True)
    name = Column(JSON, nullable=True)
    position = Column(JSON, nullable=True)
    description = Column(JSON, nullable=True)


class Resident(Base):

     __tablename__ = "resident"

     id = Column(Integer, primary_key=True)
     image_url = Column(String, index=True)
     name = Column(JSON, nullable=True)
     position = Column(JSON, nullable=True)
     description = Column(JSON, nullable=True)


class Blog(Base):

    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True)
    title = Column(JSON, nullable=True)
    sub_title = Column(JSON, nullable=True)
    blog_url = Column(String, index=True)
    image_1 = Column(String, index=True)
    image_2 = Column(String, nullable=True,index=True)
    body_1 = Column(JSON, nullable=True)
    body_2 = Column(JSON, nullable=True)



class Tariff(Base):

    __tablename__ = "tariff"

    id = Column(Integer, primary_key=True)
    space_id = Column(Integer, index=True)
    to = Column(String, index=True)
    tabs = Column(ARRAY(JSONB), index=True)
    service = Column(ARRAY(JSONB), index=True)

class Space(Base):

    __tablename__ = "space"

    id = Column(Integer, primary_key=True)
    title = Column(JSON)
    image = Column(String, index=True)

    faq = relationship("FAQ", back_populates="space")

class FAQ(Base):

    __tablename__ = "faq"

    id = Column(Integer, primary_key=True)
    question = Column(JSON)
    answer = Column(JSON)
    space_id = Column(Integer, ForeignKey("space.id"))
    space = relationship("Space", back_populates="faq")


class Translation(Base):

    __tablename__ = "translation"

    id = Column(Integer, primary_key=True)
    text = Column(JSON, nullable=True)
    image = Column(String, index=True)

class Cards_blog(Base):

    __tablename__ = "cards_blog"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, server_default=func.now())
    image = Column(String, index=True)
    title = Column(JSON, nullable=True)
    url = Column(String, index=True)


class User(Base):

    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    password = Column(String, index=True)