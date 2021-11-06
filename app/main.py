from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

from starlette.status import HTTP_201_CREATED

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [{
        "title": "title of post 1", 
        "content": "content of post 1",
        "id": 1,
        "published": True,
        "rating": 5
    },
    {
        "title": "Favorite foods", 
        "content": "My favorite food is semo",
        "id": 2,
        "published": True,
        "rating": 4
    }]


@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts", status_code=HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}
    

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = [x for x in my_posts if x['id'] == id]
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # deleting post
    # Find the index in the array of the required ID

    index = [i for i, p in enumerate(my_posts) if p['id'] == id]
    
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    
    my_posts.pop(index[0])
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    
    index = [i for i, p in enumerate(my_posts) if p['id'] == id]

    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index[0]] = post_dict
    return {"Message": "updated post"}