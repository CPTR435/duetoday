from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from alchemy.setup import Base
import datetime

class User(Base):
    __tablename__ = 'users'
    wwuid = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    mask_photo = Column(String(250))
    subscriptions = Column(String(2500))
    def to_json(self):
        return {'wwuid': str(self.wwuid), 'name': str(self.name), 'mask_photo': str(self.mask_photo), 'subscriptions': str(self.subscriptions)}

class Feed(Base):
    __tablename__ = 'feeds'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250))
    owner = Column(Integer, ForeignKey("users.wwuid"), nullable=False)
    administrators = Column(String(1000))
    private = Column(Boolean, default=True)
    def to_json(self):
        return {'id': str(self.id), 'name': str(self.name), 'description': str(self.description), 'owner': str(self.owner), 'administrators': str(self.administrators), 'private': str(self.private)}

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    feed_id = Column(Integer, ForeignKey("feeds.id"), nullable=False)
    name = Column(String(250), nullable=False)
    description = Column(String(250))
    start = Column(String(250), nullable=False)
    end = Column(String(250), nullable=False)
    creator = Column(Integer, ForeignKey("users.wwuid"), nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    def to_json(self):
        return {'id': str(self.id), 'feed_id': str(self.feed_id), 'name': str(self.name), 'description': str(self.description), 'start_time': str(self.start_time), 'end_time': str(self.end_time), 'creator': str(self.creator), 'updated_at': str(self.updated_at)}
