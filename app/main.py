# pylint: skip-file
from typing import Optional, List
from sys import displayhook
from fastapi import FastAPI,Response,status,HTTPException, Depends
from fastapi import Body
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models,schemas
from .database import engine,get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='passwod123', cursor_factory = RealDictCursor)
        cursor = conn.cursor()
        print('connected to db successful')
        break;
    except Exception as error:
        print('Connection to db failed')
        print('error = ',error)
        time.sleep(3)
        
my_posts = [{"title":"title of post1", "content":"content of post 1","id":123},{"title":"fav foods","content":"pizza","id":232}]

def find_post(id):
    for p in my_posts:
        print(p)
        if p['id'] == id:
            return p


def find_index(id): 
    for p in my_posts:
        print(p)
        if p['id'] == id:
            return my_posts.index(p)

@app.get("/")
def read_root():
    return {"Hello": "test"}

@app.get("/posts")
def get_posts(db: Session = Depends(get_db),response_model=List[schemas.Post]):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

@app.post("/posts",status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts(title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/posts/{id}",response_model=schemas.Post)
def get_one_post(id: int, response: Response, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id==id).first()
    print(post)
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""",str(id))
    # post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} not found')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message':f'post with {id} not found'}
    return post

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts where id = %s returning *""" % (str(id)),)
    # deleted_post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id==id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} not found')

    post.delete(synchronize_session=False)
    db.commit()
    return({"message": f"post {id} successfully rmemoved"})

@app.put("/posts/{id}",status_code=status.HTTP_200_OK,response_model=schemas.Post)
def update_post(id: int,updated_post: schemas.PostBase, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = \'%s\', content = \'%s\', published = %s WHERE id = %s RETURNING *""" % (post.title, post.content, post.published, str(id)),)
    # updated_post = cursor.fetchone()
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} not found')
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    # db.refresh()
    return post_query.first()

@app.post("/users",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut) # , response_model=schemas.Post)
def create_user(newuser: schemas.UserCreate,db: Session = Depends(get_db)):
    new_user = models.User(**newuser.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user