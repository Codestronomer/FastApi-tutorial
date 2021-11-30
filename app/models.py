from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import null, text
from .db import Base
from sqlalchemy import Column, Integer, String, Boolean

class Post(Base):

    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created = Column(
                        TIMESTAMP(timezone=True), 
                        nullable=False, 
                        server_default=text('NOW()')
                    )
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),  nullable=False)

    owner = relationship("User", primaryjoin="Post.owner_id == User.id")
    comments = relationship("Comment", primaryjoin="Post.id == Comment.post_id")


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created = Column(TIMESTAMP, server_default=text('NOW()'), nullable=False)


class Votes(Base):

    __tablename__ = "votes"
    
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete="CASCADE"), primary_key=True)


class Comment(Base):

    __tablename__ = "comments"

    post_id = Column(Integer, ForeignKey('posts.id', ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)
    content = Column(String, nullable=False)
    created = Column(TIMESTAMP, server_default=text('NOW()'), nullable=False)
    user = relationship('User', backref='comments', lazy=True)