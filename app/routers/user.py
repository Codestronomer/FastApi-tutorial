
from .. import schemas, utils, models
from ..db import get_db
from fastapi import status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session


router = APIRouter(
    tags=['users']
)


@router.post('/users', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # Hash the password - user.password

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get('/users', status_code=status.HTTP_200_OK, response_model=List[schemas.UserOut])
def get_users(db: Session = Depends(get_db)):

    users = db.query(models.User).all()

    return users


@router.get('/users/{id}', status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with the id: {id} not found.")

    return user