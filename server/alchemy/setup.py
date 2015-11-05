from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
import logging

Base = declarative_base()

from alchemy.base_models import *

engine = create_engine("sqlite:///data.db")

Base.metadata.create_all(engine)

Base.metadata.bind = engine
dbs = sessionmaker(bind=engine)
s = dbs()

logger = logging.getLogger("pyserver")

def addOrUpdate(thing):
    try:
        s.add(thing)
        s.commit()
        return thing
    except Exception as e:
        logger.info(e)
        s.rollback()

def query_all(model):
    thing = None
    try:
        thing = s.query(model).all()
    except Exception as e:
        logger.info(e)
        s.rollback()
    return thing

def query_by_wwuid(model, wwuid):
    thing = None
    try:
        thing = s.query(model).filter_by(wwuid=wwuid).all()
    except Exception as e:
        logger.info(e)
        s.rollback()
    return thing

def query_by_id(model, id):
    thing = None
    try:
        thing = s.query(model).filter_by(id=id).first()
    except Exception as e:
        logger.info(e)
        s.rollback()
    return thing

def query_by_field(model, field, value):
    thing = None
    try:
        thing = s.query(model).filter(getattr(model, field).like(value)).all()
    except Exception as e:
        logger.info(e)
        s.rollback()
    return thing

def query_user(wwuid):
    thing = query_by_wwuid(User, wwuid)
    if thing:
        thing = thing[0]
    return thing

def delete_thing(thing):
    try:
        s.delete(thing)
        s.commit()
    except Exception as e:
        logger.info(e)
        s.rollback()
