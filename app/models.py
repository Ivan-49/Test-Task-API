from sqlalchemy import Column, Integer, String, DateTime, Float

# from sqlalchemy.orm import relationship

from .database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    article = Column(String, index=True)
    price = Column(Integer)
    rating = Column(Float, nullable=True)
    total_quantity = Column(Integer, nullable=True)
    datetime = Column(DateTime(timezone=True))

    # items = relationship("Item", back_populates="owner")


class ScheduledTask(Base):
    __tablename__ = "scheduled_tasks"

    id = Column(Integer, primary_key=True, index=True)
    article = Column(String, index=True)
