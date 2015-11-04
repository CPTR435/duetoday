from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from alchemy.setup import Base
import datetime

class User(Base):
    __tablename__ = 'users'
    wwuid = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

class Feed(Base):
    __tablename__ = 'feeds'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250))
    owner = Column(Integer, ForeignKey("users.wwuid"), nullable=False)
    private = Column(Boolean, default=True)

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    feed_id = Column(Integer, ForeignKey("feeds.id"), nullable=False)
    name = Column(String(250), nullable=False)
    description = Column(String(250))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    creator = Column(Integer, ForeignKey("users.wwuid"), nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
