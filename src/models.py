from dataclasses import dataclass

from src import Base, engine
from sqlalchemy import Column, Integer, String,Float


@dataclass
class Book:
    title: str
    price: float
    stock: int
    rating: int
    description: str
    url : str
    product_type: str
    product_incl_tax: float
    product_excl_tax: float
    tax : float
    total_reviews: int
    img_url: str

class BookSQL(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(Float)
    stock = Column(Integer)
    rating = Column(Integer)
    description = Column(String)
    url = Column(String)
    product_type = Column(String)
    product_incl_tax = Column(Float)
    product_excl_tax = Column(Float)
    tax = Column(Float)
    total_reviews = Column(Integer)
    img_url = Column(String)

try:
    Base.metadata.create_all(engine)
except Exception as e:
    print(e)
    