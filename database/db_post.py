from routers.schemas import PostBase
from sqlalchemy.orm.session import Session
import datetime
from database.models import DbPost
from fastapi import HTTPException, status
import os

def create(db: Session, request: PostBase):
    new_post = DbPost(
        title=request.title,
        content=request.content,
        creator=request.creator,
        image_url=request.image_url,
        timestamp=datetime.datetime.now()
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

def get_all(db: Session):
    return db.query(DbPost).all()

def delete(db: Session, id: int):
    post = db.query(DbPost).filter(DbPost.id == id).first()
    if not post:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} not found!")
    
    image_folder = 'images'
    filename = post.image_url
    
    os.remove(filename)
    
    db.delete(post)
    db.commit()
    return 'ok'

