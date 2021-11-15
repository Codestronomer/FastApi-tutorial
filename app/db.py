from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from .config import settings
# import psycopg2
# import time
# import os

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.db_username}:{settings.db_password}@{settings.db_hostname}/{settings.db_name}'

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


# Connecting to the database without sqlalchemy

# user = os.getenv('USER')
# password = os.getenv('PASSWORD')

# while True:

#     try:
#         conn = psycopg2.connect(
#             host='localhost', 
#             database='fastapi-tut', 
#             user=f'{user}', 
#             password=f'{password}',
#             cursor_factory=RealDictCursor
#         )
#         cursor = conn.cursor()
#         print("Database connection was successful.")
#         break

#     except Exception as error:
#         print("Connecting to the database failed")
#         print("Error", error)
#         time.sleep(10.0)
