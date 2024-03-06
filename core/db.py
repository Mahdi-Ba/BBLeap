import redis
from sqlalchemy import create_engine,MetaData
from sqlalchemy.ext.declarative import declarative_base
from core.settings import Settings
from databases import Database
DATABASE_URL = Settings.DATABASE_URL
database = Database(DATABASE_URL)
metadata = MetaData()
engine = create_engine(DATABASE_URL)
Base = declarative_base()
from sqlalchemy.orm import Session


def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()


# Initialize a Redis client
redis_client = redis.Redis(host=Settings.REDIS_HOST, port=6379, db=0, decode_responses=True)
