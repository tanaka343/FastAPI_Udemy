from database import Base
from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer,primary_key=True)
    name = Column(String,nullable=False)
    email = Column(String,nullable=True)
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)

    user = relationship("User",back_populates="items")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True)
    name = Column(String,unique=True,nullable=False)
    password = Column(String,unique=True,nullable=False)
    salt = Column(String,nullable=False)

    items = relationship("Item",back_populates="user")