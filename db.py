from os import getenv
from pathlib import Path

from databases import Database
from dotenv import load_dotenv
from starlette.config import Config

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

DB_USER = getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = getenv("POSTGRES_PASSWORD", "newpassword")
DB_HOST = getenv("POSTGRES_SERVER", "postgres_db")
DB_NAME = getenv("POSTGRES_DB", "staysynergy")
DB_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@postgres_db:5432/{DB_NAME}'

database = Database(DB_URL)

engine = create_engine(
    DB_URL
)
async def connect_to_db():
    """Connect to database"""
    await database.connect()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()