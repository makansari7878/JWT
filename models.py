from database import Base
from sqlalchemy import Column, Integer, String

class Users(Base):
    __tablename__ = 'users123'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)