from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
import time
import os
from psycopg2.extras import RealDictCursor
from starlette.status import HTTP_201_CREATED
from . import models
from sqlalchemy.orm import Session
from fastapi import Depends
from .db import engine, get_db

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True



user = os.getenv('USER')
password = os.getenv('PASSWORD')

while True:

    try:
        conn = psycopg2.connect(
            host='localhost', 
            database='fastapi-tut', 
            user=f'{user}', 
            password=f'{password}',
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("Database connection was successful.")
        break

    except Exception as error:
        print("Connecting to the database failed")
        print("Error", error)
        time.sleep(10.0)


@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()
    return {'data':posts }



@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts;""")
    posts = cursor.fetchall()
    
    return {"data": posts}



@app.post("/posts", status_code=HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute(
        """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
        (post.title, post.content, post.published)
    )
    new_post = cursor.fetchone()
    
    conn.commit()

    return {"data": new_post}
    

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # deleting post
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    
    cursor.execute(
        """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
        (post.title, post.content, post.published, str(id))
    )
    updated_post = cursor.fetchone()
    conn.commit()

    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    return {"Message": updated_post}


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
