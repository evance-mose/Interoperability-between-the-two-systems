from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pymongo import mongo_client
import pymongo
from config import settings

# mysql connection
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root@localhost:3307/hospital"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# mongo connection
client = mongo_client.MongoClient(settings.DATABASE_URL)

db = client[settings.MONGO_INITDB_DATABASE]
Patients = db["patients"]

Patients.create_index([("ssn", pymongo.ASCENDING)], unique=True)
