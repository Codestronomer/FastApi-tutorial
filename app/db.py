from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

user = os.getenv('USER')
password = os.getenv('PASSWORD')
SQLALCHEMY_DATABASE_URL = f'postgresql://{user}:{password}@localhost/fastapi-tut'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() 


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()