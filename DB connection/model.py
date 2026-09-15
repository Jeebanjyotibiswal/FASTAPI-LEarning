from sqlalchemy import Column, String, Integer
from main import Base

class Todos(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    completed = Column(String)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    name= Column(String)
    age= Column(Integer)