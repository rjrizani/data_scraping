from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

BASE_URL = "https://books.toscrape.com/"

DATABASE_URL = "sqlite:///books.db"

engine = create_engine(DATABASE_URL)
Base = declarative_base()


