from sqlalchemy import  create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import  declarative_base

SQLALCHEMY_DB = 'sqlite:///./toolsapp.db'
engine = create_engine(SQLALCHEMY_DB, connect_args={'check_same_thread':False})

SessionLocal = sessionmaker(autoflush=False, bind=engine, autocommit = False)
Base = declarative_base()