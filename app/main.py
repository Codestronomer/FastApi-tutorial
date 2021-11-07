import os
import time
import psycopg2
from fastapi import Depends
from . import models, schemas
from .db import engine, get_db
from fastapi.params import Body
from typing import Optional, List
from sqlalchemy.orm import Session
from psycopg2.extras import RealDictCursor
from starlette.status import HTTP_201_CREATED
from fastapi import FastAPI, Response, status, HTTPException


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


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


@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()

    # cursor.execute("""SELECT * FROM posts;""")
    # posts = cursor.fetchall()
    
    return posts



@app.post("/posts", status_code=HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):

    # cursor.execute(
    #     """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #     (post.title, post.content, post.published)
    # )
    # new_post = cursor.fetchone()
    # conn.commit()

    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post
    

@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # deleting post

    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    
    # cursor.execute(
    #     """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #     (post.title, post.content, post.published, str(id))
    # )
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    post_query.update(updated_post.dict(), synchronize_session=False)
    
    db.commit()
    return post_query.first()


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
