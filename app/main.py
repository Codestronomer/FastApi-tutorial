import os
import time
import psycopg2
from . import models, schemas, utils
from .db import engine, get_db
from fastapi.params import Body
from sqlalchemy.orm import Session
from .routers import post, user, auth
from psycopg2.extras import RealDictCursor
from starlette.status import HTTP_201_CREATED
from fastapi import FastAPI


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Hello World!"}

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



# my_posts = [{
#         "title": "title of post 1", 
#         "content": "content of post 1",
#         "id": 1,
#         "published": True,
#         "rating": 5
#     },
#     {
#         "title": "Favorite foods", 
#         "content": "My favorite food is semo",
#         "id": 2,
#         "published": True,
#         "rating": 4
