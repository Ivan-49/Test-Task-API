from sqlalchemy import Column, Integer, String, DateTime, Float

from .database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    artikul = Column(String)
    name = Column(String)
    standart_price = Column(Float)
    sell_price = Column(Float)
    total_quantity = Column(Integer)
    datetime = Column(DateTime)
    rating = Column(Float)


class Subscribe(Base):
    __tablename__ = "subs"

    id = Column(Integer, primary_key=True, index=True)
    artikul = Column(String)
