from database import Base
from sqlalchemy import Column,Integer,String


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer,primary_key=True)
    name = Column(String,nullable=False)
    email = Column(String,nullable=True)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True)
    name = Column(String,unique=True,nullable=False)
    password = Column(String,unique=True,nullable=False)