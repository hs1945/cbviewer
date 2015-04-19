from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine, Column, Integer, String, DateTime

DeclarativeBase = declarative_base()

DATABASE = {
    'drivername': 'postgres',
    'host': 'localhost',
    'port': '5432',
    'username': 'postgres',
    'password': '',
    'database': 'crunchbase'
}

def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.DATABASE))

def create_company_table(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)

class Company(DeclarativeBase):
    """Sqlalchemy deals model"""
    __tablename__ = "company"

    id = Column(Integer, primary_key=True)
    name = Column('name', String)
    permalink = Column('permalink', String, nullable=True)
    location = Column('location', String, nullable=True)
    