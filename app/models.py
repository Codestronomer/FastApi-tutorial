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
    created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()'))


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created = Column(TIMESTAMP, server_default=text('NOW()'), nullable=False)

