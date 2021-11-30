from typing import List
from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm.session import Session
from ..db import get_db
from ..oauth2 import get_current_user
from .. import schemas, models

router = APIRouter(prefix='/comments', tags=['comments'])


@router.post('/', response_model=schemas.Comment, status_code=status.HTTP_201_CREATED)
def create_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == comment.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {comment.post_id} does not exist.")
    
    new_comment = models.Comment(
                            post_id = comment.post_id,
                            user_id = current_user.id,
                            content = comment.content)
    
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment


@router.get('/{id}', response_model=List[schemas.Comment], status_code=status.HTTP_200_OK)
def get_comments(id: int, db: Session = Depends(get_db)):
    comments = db.query(models.Comment).filter(models.Comment.post_id == id).all()

    return comments
