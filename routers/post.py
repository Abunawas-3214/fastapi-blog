from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session
from database.database import get_db
from database import db_post
from routers.schemas import PostBase
import random
import string
import shutil

router = APIRouter(
    prefix="/post",
    tags=["post"]  
)

@router.post("/")
def create(request: PostBase, db: Session = Depends(get_db)):
    return db_post.create(db, request)

@router.get("/")
def all(db: Session = Depends(get_db)):
    return db_post.get_all(db)

@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    return db_post.delete(db, id)

@router.post("/image")
def create_image(image: UploadFile, db: Session = Depends(get_db)):
    random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        
    new = f'_{random_string}.'
    filename = new.join(image.filename.rsplit('.', 1))
    path = f'./images/{filename}'
    
    with open(path, 'w+b') as buffer:
        shutil.copyfileobj(image.file, buffer)
        
    return {'filename': path}
        


 