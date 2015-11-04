from sqlalchemy import Column, ForeignKey, Integer, String
from alchemy.setup import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class Feed(Base):
    __tablename__ = 'feeds'
    id = Column(Integer, primary_key=True)


class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    feed_id = Column(Integer, ForeignKey("feeds.id"), nullable=False)
